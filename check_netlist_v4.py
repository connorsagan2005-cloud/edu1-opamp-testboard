"""Check KiCad's exported XML connectivity against the v4 Markdown source.
Run: python check_netlist_v4.py [opamp_block.net.xml]
Requires PyYAML. Export a fresh XML netlist with KiCad before checking edits.
This checks capture correctness, not electrical stability or MIL compliance.
"""
import sys,re,json,collections
from pathlib import Path
import xml.etree.ElementTree as ET
import yaml
sys.path.insert(0,str(Path(__file__).resolve().parent/'tools'))
from sexpr import parse,children,one
base=Path(__file__).resolve().parent
spec=(base/'EDU1_Opamp_Block_Spec_v4.md').read_text()
blocks=[yaml.safe_load(b) for b in re.findall(r'```yaml\n(.*?)```',spec,re.S)]
cs={};nets={}
for b in blocks:
    cs.update({c['ref']:c for c in b.get('components',[])})
    nets.update(b.get('nets',{}))
def dup(s):return re.sub(r'^(CH|OP|op|JP|SW|TP|R|C|U|J)1',r'\g<1>2',s)
for ref,c in list(cs.items()):
    if re.match(r'^(R|C|SW|U|TP|J|JP)1',ref):cs[dup(ref)]={**c,'ref':dup(ref)}
for net,members in list(nets.items()):
    if net.startswith(('CH1_','OP1_')):nets[dup(net)]=[dup(x) for x in members]
expected={k:{m for m in v if '.' in m} for k,v in nets.items()}
external={m:k for k,v in nets.items() for m in v if '.' not in m}
assert len(cs)==118 and len(nets)==64 and len(external)==8
r=ET.parse(sys.argv[1] if len(sys.argv)>1 else base/'opamp_block.net.xml').getroot()
actualcs={c.get('ref'):c for c in r.findall('./components/comp')}
assert set(actualcs)==set(cs),('Component set mismatch',set(cs)^set(actualcs))
actual={};seen=collections.Counter()
for net in r.findall('./nets/net'):
    name=net.get('name').rsplit('/',1)[-1]
    assert name not in actual,('Duplicate net basename',name)
    members=[]
    for node in net.findall('node'):
        ref=node.get('ref');pin=node.get('pin')
        if cs[ref]['type']=='OPAMP':pin={'1':'+','2':'-','3':'V+','4':'V-','5':'OUT'}[pin]
        member=ref+'.'+pin;members.append(member);seen[member]+=1
    actual[name]=set(members)
assert set(actual)==set(expected),('Net-name mismatch',set(actual)^set(expected))
for n in expected:assert actual[n]==expected[n],(n,'missing',expected[n]-actual[n],'extra',actual[n]-expected[n])
assert all(v==1 for v in seen.values()),'Pins appear on multiple nets'
for ref,c in cs.items():assert actualcs[ref].findtext('value','')==(c.get('value') or '~'),(ref,'value mismatch')
sheets={n:parse((base/n).read_text()) for n in ['opamp_block.kicad_sch','opamp_ch1.kicad_sch','opamp_ch2.kicad_sch']}
roots=sheets['opamp_block.kicad_sch']; childnodes=children(roots,'sheet')
assert len(childnodes)==2
assert {str(next(p[2] for p in children(s,'property') if p[1]=='Sheetfile')) for s in childnodes}=={'opamp_ch1.kicad_sch','opamp_ch2.kicad_sch'}
assert {h[1] for h in children(roots,'hierarchical_label')}==set(external)
assert len(children(roots,'hierarchical_label'))==8
for h in children(roots,'hierarchical_label'):
    assert one(h,'shape')[1]==('input' if h[1] in ['vaa','agnd'] else 'passive')
counts=[];dnp=0;allrefs=set()
for name,s in sheets.items():
    assert not children(s,'global_label'),name+' contains global labels'
    if name!='opamp_block.kicad_sch':assert not children(s,'sheet')
    symbols=children(s,'symbol');counts.append(len(symbols))
    for sym in symbols:
        props={p[1]:p[2] for p in children(sym,'property')};ref=props['Reference'];allrefs.add(ref)
        assert props['Footprint']=='',(ref,'assigned footprint')
        assert props['Value']==cs[ref].get('value','')
        assert props.get('Tolerance')==cs[ref].get('tol')
        fitted=one(sym,'dnp')[1]=='no';assert fitted==cs[ref]['fitted'],(ref,'DNP mismatch')
        dnp+=not fitted
assert counts==[12,53,53],counts
assert allrefs==set(cs)
assert not {'DUT','J_VAA','JP_IVAA','J_SCAN','R_GNDLINK'}&allrefs
print('PASS: actual KiCad XML export matches v4 pin membership on every net.')
print('Components: 118 = 12 support + 53 channel 1 + 53 channel 2')
print('Nets: 64 = 6 support + 29 channel 1 + 29 channel 2')
print('External hierarchical labels: 8; child sheets: 2; global labels: 0')
print(f'Component pins checked: {len(seen)}; duplicate/missing/extra pin memberships: 0')
print(f'DNP components: {dnp}; all values, tolerance fields and empty footprints verified.')
print('TBD/TBD-AD:',', '.join(ref+'='+c['value'] for ref,c in cs.items() if c.get('value') in ['TBD','TBD-AD']))
print('Op-amp values: U_REF, U1_NULL, U2_NULL = ZERO_DRIFT_RRIO_TBD')
