"""Repository policy lint plus own-package smoke test; not a full security scanner."""
from __future__ import annotations
import ast
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
import build_release
import scavenger

ROOT=Path(__file__).resolve().parents[1]
RUNTIME=('scripts/scavenger.py','scripts/guardrails.py')
ALLOWED={'__future__','argparse','json','re','sys','datetime','pathlib','typing','urllib.parse','guardrails','math','os','stat'}


def audit(root: Path) -> dict:
    findings=[]
    names=build_release.files(root)
    for name in RUNTIME:
        tree=ast.parse((root/name).read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            modules=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) else []
            if any(m not in ALLOWED for m in modules):findings.append(name+': import requires review')
            if isinstance(node,ast.Call):
                call=node.func
                if isinstance(call,ast.Name) and call.id in {'eval','exec','compile','__import__'}:
                    findings.append(name+': dynamic execution')
                if isinstance(call,ast.Attribute) and (call.attr in {'system','popen'} or call.attr.startswith(('exec','spawn'))):
                    findings.append(name+': process execution')
    secret=re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
    scanned=0
    for name in names:
        path=root/name;content=path.read_text(encoding='utf-8');scanned+=1
        # Avoid matching the detector's own literal pattern; no real fixture secrets.
        if secret.search(content):findings.append(name+': possible credential; review privately')
        if name.endswith('.md'):
            for target in re.findall(r'\]\(([^)]+)\)',content):
                if '://' in target or target.startswith('#'):continue
                linked=(path.parent/target.split('#',1)[0]).resolve()
                if not linked.is_relative_to(root.resolve()) or not linked.exists():
                    findings.append(name+': broken/escaping local link')
        if name.startswith('.github/workflows/'):
            if 'pull_request_target' in content:findings.append(name+': unsafe trigger')
            for action in re.findall(r'uses:\s*([^\s]+)',content):
                if not re.fullmatch(r'[\w./-]+@[0-9a-f]{40}',action):findings.append(name+': unpinned action')
            if 'persist-credentials: false' not in content:findings.append(name+': checkout credential persistence')
    version=(root/'VERSION').read_text().strip();skill=(root/'SKILL.md').read_text()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-rc\.\d+)?',version):findings.append('Invalid version')
    if 'version: "'+version+'"' not in skill or '\nlicense: MIT\n' not in skill:findings.append('Skill metadata mismatch')
    if 'Permission is hereby granted, free of charge' not in (root/'LICENSE').read_text():findings.append('Missing license grant')
    scavenger.check_skill(root)
    if findings:raise ValueError('; '.join(findings))
    return {'files_scanned':scanned,'runtime_modules_inspected':list(RUNTIME),
            'policy_findings':0,'limitation':'Allowlist/AST/known-pattern lint only; not comprehensive SAST, secret scanning, or a security guarantee.'}


def smoke(root: Path) -> dict:
    with tempfile.TemporaryDirectory() as directory:
        temp=Path(directory).resolve();one=temp/'one.zip';two=temp/'two.zip'
        digest=build_release.build(root,one)
        if digest!=build_release.build(root,two) or one.read_bytes()!=two.read_bytes():
            raise ValueError('Build is not reproducible')
        # Only execute our just-built, verified package, never arbitrary downloaded archives.
        unpack=temp/'unpacked';unpack.mkdir()
        for name,data in build_release.verify(one).items():
            target=unpack/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        skill=unpack/'scavenger';work=temp/'research workspace'
        commands=[['check-skill',str(skill)],['validate',str(skill/'examples/demo-record.json')],
                  ['score',str(skill/'examples/demo-record.json')],['init',str(work),'--name','Package smoke'],
                  ['validate',str(work/'research-record.json')]]
        for args in commands:
            result=subprocess.run([sys.executable,str(skill/'scripts/scavenger.py'),*args],cwd=temp,
                                  capture_output=True,text=True,timeout=15)
            if result.returncode:raise ValueError('Installed-package smoke failed: '+result.stderr)
        return {'reproducible':True,'sha256':digest,'package_files':len(build_release.verify(one)),
                'smoke_commands_passed':len(commands),'agent_host_installation_tested':False}


if __name__=='__main__':
    try:print(json.dumps({'audit':audit(ROOT),'package':smoke(ROOT)},indent=2))
    except (OSError,ValueError,subprocess.SubprocessError) as exc:
        print('Release check failed: '+str(exc),file=sys.stderr);raise SystemExit(2)
