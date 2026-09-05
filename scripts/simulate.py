"""Deterministic record simulations, NOT agent/model evaluations."""
from __future__ import annotations
import copy
import itertools
import json
import random
import sys
from pathlib import Path
import scavenger as s


def run() -> dict:
    original = s.load(Path(__file__).resolve().parents[1] / 'examples/demo-record.json')
    scenarios = []
    def expect(name, record, rejected=False):
        try:
            s.validate(record)
        except s.Invalid:
            if not rejected: raise AssertionError(name + ': unexpected rejection')
        else:
            if rejected: raise AssertionError(name + ': invalid record accepted')
        scenarios.append({'case': name, 'result': 'pass'})
    expect('complete synthetic handoff', original)
    r=copy.deepcopy(original);r['decisions'][0].update(disposition='gap', candidate_ids=[])
    expect('sparse research retains explicit gap',r)
    for gate in s.GATES:
        r=copy.deepcopy(original);r['candidates'][0]['gates'][gate]='unknown'
        expect('unknown '+gate+' blocks reuse',r,True)
    r=copy.deepcopy(original);r['decisions']=[]
    expect('missing requirement disposition',r,True)
    r=copy.deepcopy(original);r['candidates'][0]['evidence'][0]['level']='documented'
    expect('documentation alone cannot authorize code reuse',r,True)
    r=copy.deepcopy(original);r['project']['synthetic']=False
    expect('synthetic source cannot masquerade as live research',r,True)
    r=copy.deepcopy(original);r['sources'][0]['accessed_on']='2027-01-01'
    expect('observation later than report as-of',r,True)
    r=copy.deepcopy(original);r['candidates'][0]['evidence'][0]['claim']='A fabricated claim can still be structurally valid.'
    expect('documented limitation: structure cannot verify truth',r)
    assert all(not x['evidence_truth_verified'] for x in s.score(r))

    gates_checked=0
    for states in itertools.product(('pass','unknown','fail'),repeat=5):
        r=copy.deepcopy(original);r['decisions'][0]['disposition']='reference-only'
        r['candidates'][0]['gates']=dict(zip(s.GATES,states))
        row=next(x for x in s.score(r) if x['id']=='C-001')
        expected='blocked' if 'fail' in states else 'review-required' if 'unknown' in states else 'eligible'
        if row['status']!=expected or (row['score'] is not None)!=(expected=='eligible'):
            raise AssertionError('gate invariant violated')
        gates_checked+=1

    seed=20260905; randomizer=random.Random(seed)
    invalid_values=[-10,-1,6,100,True,False,'5',[],{},2.5]
    for _ in range(1000):
        r=copy.deepcopy(original)
        key=randomizer.choice(list(s.WEIGHTS))
        r['candidates'][0]['scores'][key]=randomizer.choice(invalid_values)
        try:s.validate(r)
        except s.Invalid:pass
        else:raise AssertionError('invalid score mutation accepted')
    return {'kind':'offline-deterministic-simulation','seed':seed,'scenarios':scenarios,
            'gate_combinations_checked':gates_checked,'invalid_score_mutations_rejected':1000,
            'agent_runs':0,'live_research_runs':0,'status':'pass',
            'limitation':'Tests declared records, not factual accuracy, prompt-injection resistance, or host behavior.'}


if __name__=='__main__':
    try:print(json.dumps(run(),indent=2))
    except (AssertionError,s.Invalid,OSError) as exc:
        print('Simulation failed: '+str(exc),file=sys.stderr);raise SystemExit(2)
