"""Build a deterministic allowlisted skill ZIP; verification does not execute its contents."""
from __future__ import annotations
import argparse
import hashlib
import re
import stat
from pathlib import Path, PurePosixPath
import zipfile

ROOT=Path(__file__).resolve().parents[1]
LIMIT=25_000_000


def safe_name(name: str) -> bool:
    p=PurePosixPath(name)
    return (bool(name) and '\\' not in name and ':' not in name and not p.is_absolute()
            and all(part not in ('','..','.') for part in name.split('/')))


def files(root: Path) -> list[str]:
    names=(root/'release-files.txt').read_text(encoding='utf-8').splitlines()
    if not names or len(names)!=len(set(names)) or any(not safe_name(n) for n in names):
        raise ValueError('Invalid release allowlist')
    return sorted(names)


def build(root: Path, destination: Path) -> str:
    payload={}
    for name in files(root):
        p=root/name
        if any(part.is_symlink() for part in (p,*p.parents)):
            raise ValueError('Symlinks are not allowed in a release')
        if not p.is_file() or not p.resolve().is_relative_to(root.resolve()):
            raise ValueError('Release source must be a contained regular file')
        if p.stat().st_size>LIMIT:raise ValueError('Release source too large')
        with p.open('rb') as handle:data=handle.read(LIMIT+1)
        if len(data)>LIMIT:raise ValueError('Release source too large')
        payload['scavenger/'+name]=data
    if sum(map(len,payload.values()))>LIMIT:raise ValueError('Release exceeds size limit')
    manifest=''.join(hashlib.sha256(data).hexdigest()+'  '+name+'\n' for name,data in sorted(payload.items()))
    payload['scavenger/MANIFEST.sha256']=manifest.encode('utf-8')
    # Refuse overwrite; caller owns destination.parent. Fixed metadata and no compression.
    with destination.open('xb') as handle, zipfile.ZipFile(handle,'w',compression=zipfile.ZIP_STORED) as archive:
        for name,data in sorted(payload.items()):
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0))
            info.create_system=3;info.external_attr=(stat.S_IFREG | 0o644)<<16
            archive.writestr(info,data)
    verify(destination)
    return hashlib.sha256(destination.read_bytes()).hexdigest()


def verify(path: Path) -> dict[str, bytes]:
    payload={};total=0
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            name=info.filename
            if (not safe_name(name) or not name.startswith('scavenger/') or name in payload
                or stat.S_ISLNK(info.external_attr>>16) or info.is_dir()):
                raise ValueError('Unsafe or duplicate archive member')
            if info.file_size>LIMIT:raise ValueError('Archive member too large')
            with archive.open(info) as handle:data=handle.read(LIMIT+1)
            total+=len(data)
            if total>LIMIT or len(data)!=info.file_size:raise ValueError('Invalid archive size')
            payload[name]=data
    raw=payload.pop('scavenger/MANIFEST.sha256',None)
    if raw is None:raise ValueError('Missing manifest')
    declared={}
    for line in raw.decode('utf-8').splitlines():
        digest,separator,name=line.partition('  ')
        if not separator or not re.fullmatch('[a-f0-9]{64}',digest) or name in declared:
            raise ValueError('Invalid manifest entry')
        declared[name]=digest
    if set(declared)!=set(payload):raise ValueError('Manifest member mismatch')
    if any(hashlib.sha256(data).hexdigest()!=declared[name] for name,data in payload.items()):
        raise ValueError('Manifest checksum mismatch')
    return payload


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination',type=Path)
    parser.add_argument('--verify',action='store_true')
    args=parser.parse_args()
    try:
        if args.verify:print(f'Verified {len(verify(args.destination))} files; checksums are not signatures.')
        else:print(build(ROOT,args.destination))
        return 0
    except (OSError,ValueError,zipfile.BadZipFile) as exc:
        print(type(exc).__name__+': release operation failed');return 2


if __name__=='__main__':raise SystemExit(main())
