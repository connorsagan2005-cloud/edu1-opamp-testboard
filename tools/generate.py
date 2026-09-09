from pathlib import Path
import sys,re,yaml,json,uuid,copy,math
from sexpr import parse,dump,Q,children,one
OUT=Path(__file__).resolve().parents[1]
SPEC=OUT/'EDU1_Opamp_Block_Spec_v4.md'
LIB=Path(sys.argv[1])
blocks=[yaml.safe_load(x) for x in re.findall(r'```yaml\n(.*?)```',SPEC.read_text(),re.S)]
cs=[]; nets={}; groups=[]
for b in blocks:
    if 'components' in b: groups.append(b['components']);cs+=b['components']
    nets.update(b.get('nets',{}))
def ch2(s):
    return re.sub(r'^(CH|OP|op|JP|SW|TP|R|C|U|J)1',r'\g<1>2',s)
cs+= [{**c,'ref':ch2(c['ref'])} for g in groups[1:] for c in g]
for k,v in list(nets.items()):
    if k.startswith(('CH1','OP1')): nets[ch2(k)]=[ch2(m) for m in v]
assert len(cs)==118 and len(nets)==64
pinmaps={'R':['1','2'],'C':['1','2'],'SW':['1','2'],'JP':['1','2'],'J1':['1'],'TP':['1'],'SMA':['1','2'],'OPAMP':['+','-','V+','V-','OUT']}
lookup={m:k for k,v in nets.items() for m in v}
assert sum(len(v) for v in nets.values())==len(lookup)
for c in cs:
    assert all(c['ref']+'.'+p in lookup for p in pinmaps[c['type']]),c
ids={'R':'Device:R','C':'Device:C','SW':'Switch:SW_SPST','JP':'Connector_Generic:Conn_01x02','TP':'Connector:TestPoint','J1':'Connector_Generic:Conn_01x01','SMA':'Connector:Conn_Coaxial','OPAMP':'Simulation_SPICE:OPAMP'}
syms={}; pins={}
for typ,libid in ids.items():
    lib,name=libid.split(':'); tree=parse((LIB/(lib+'.kicad_sym')).read_text())
    sym=copy.deepcopy(next(x for x in children(tree,'symbol') if x[1]==name))
    sym[1]=Q(libid)
    # Strip only KiCad 9 metadata and simulation properties, retaining generic graphics/pins.
    def clean(a):
        if a and a[0] in ['pin_numbers','pin_names','pin']:
            a[:]=['hide' if x==['hide','yes'] else x for x in a]
        a[:]=[x for x in a if not (isinstance(x,list) and (x[0]=='embedded_fonts' or (x[0]=='property' and str(x[1]).startswith('Sim.'))))]
        for x in a:
            if isinstance(x,list):clean(x)
    clean(sym)
    for prop in children(sym,'property'):
        if prop[1] in ['Footprint','Datasheet']:prop[2]=Q('')
    pp=[]
    for unit in children(sym,'symbol'):
        for p in children(unit,'pin'):
            num=str(one(p,'number')[1]); semantic=num
            if typ=='OPAMP':semantic={'1':'+','2':'-','3':'V+','4':'V-','5':'OUT'}[num]
            pp.append((num,semantic,*map(float,one(p,'at')[1:4])))
    assert {x[1] for x in pp}==set(pinmaps[typ]),(typ,pp)
    pins[typ]=pp;syms[typ]=dump(sym)
# Bundle the actual generic symbols so later library edits work without any custom DUT library.
for lib in set(x.split(':')[0] for x in ids.values()):
    entries=[]
    for typ,libid in ids.items():
        if libid.startswith(lib+':'):
            a=parse(syms[typ]);a[1]=Q(libid.split(':')[1]);entries.append(dump(a))
    (OUT/(lib+'.kicad_sym')).write_text('(kicad_symbol_lib (version 20231120) (generator kicad_symbol_editor)\n'+'\n'.join(entries)+'\n)')
(OUT/'sym-lib-table').write_text('(sym_lib_table\n'+'\n'.join(f'(lib (name "{l}") (type "KiCad") (uri "${{KIPRJMOD}}/{l}.kicad_sym") (options "") (descr "Generic symbols bundled for portability"))' for l in sorted(set(x.split(':')[0] for x in ids.values())))+'\n)')
def uid():return str(uuid.uuid4())
def q(s):return json.dumps(s)
def fx(size=1.27,justify='',hide=False):return f'(effects (font (size {size} {size})) '+(f'(justify {justify}) ' if justify else '')+('(hide yes)' if hide else '')+')'
def txt(s,x,y,size=1.5):return f'(text {q(s)} (at {x} {y} 0) {fx(size,"left top")} (uuid "{uid()}"))'
def wire(a,b):return f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width 0) (type default)) (uuid "{uid()}"))'
def label(s,x,y,angle=0):return f'(label {q(s)} (at {x} {y} 0) {fx(1.0,"right bottom" if angle==180 else "left bottom")} (uuid "{uid()}"))'
def hlabel(s,x,y,shape='passive'):return f'(hierarchical_label {q(s)} (shape {shape}) (at {x} {y} 180) {fx(1.27,"right")} (uuid "{uid()}"))'
def prop(n,v,x,y,hide=False,size=1.15):return f'(property {q(n)} {q(v)} (at {x} {y} 0) {fx(size,"left",hide)})'
root=uid(); childids=[uid(),uid()]
def comp(c,x,y,path):
    t=c['type']; ref=c['ref']; value=c.get('value',''); u=uid()
    z=[f'(symbol (lib_id "{ids[t]}") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp {"no" if c["fitted"] else "yes"}) (uuid "{u}")',prop('Reference',ref,x+10.16,y-6.35),prop('Value',value,x+10.16,y-3.81),prop('Footprint','',x,y,True),prop('Datasheet','',x,y,True),prop('Fitted',str(c['fitted']).lower(),x,y,True)]
    if 'tol' in c:z.append(prop('Tolerance',c['tol'],x+10.16,y-1.27))
    if 'mil' in c:z.append(prop('MIL',c['mil'],x,y,True))
    for num,*_ in pins[t]:z.append(f'(pin "{num}" (uuid "{uid()}"))')
    z.append(f'(instances (project "opamp_block" (path "{path}" (reference "{ref}") (unit 1)))))')
    for num,semantic,px,py,angle in pins[t]:
        a=(round(x+px,4),round(y-py,4));rad=math.radians(angle)
        b=(round(a[0]-5.08*math.cos(rad),4),round(a[1]+5.08*math.sin(rad),4))
        z.append(wire(a,b));z.append(label(lookup[ref+'.'+semantic],*b,180 if angle==0 else 0))
    return '\n'.join(z)
def sheetstart(u,title,types):
    return [f'(kicad_sch (version 20231120) (generator eeschema) (uuid "{u}") (paper "A2") (title_block (title {q(title)}) (rev "4") (company "WPI - EDU1 Op-amp characterization"))','(lib_symbols '+'\n'.join(syms[t] for t in sorted(types))+')']
shared=groups[0]
a=sheetstart(root,'Op-amp block | REF, AUX supply and 8-pin interface',set(c['type'] for c in shared))
a.append(txt('OPAMP BLOCK  /  SHARED SUPPORT + EXTERNAL INTERFACE',15.24,15.24,3))
a.append(txt('8 hierarchical labels become border pins when this sheet is inserted into the master project.',15.24,25.4))
for i,c in enumerate(shared):a.append(comp(c,45.72+(i%4)*127,60.96+(i//4)*38.1,'/'+root))
ext={'vaa':'VAA','agnd':'AGND',**{f'op{n}_{p}':f'OP{n}_{p.upper()}' for n in [1,2] for p in ['inp','inn','out']}}
for i,(p,net) in enumerate(ext.items()):
    y=198.12+i*12.7;a.extend([hlabel(p,45.72,y,'input' if p in ['vaa','agnd'] else 'passive'),wire((45.72,y),(76.2,y)),label(net,76.2,y)])
for n,su in enumerate(childids,1):
    x=203.2+(n-1)*177.8;y=198.12;w=101.6;h=96.52
    ports=['REF','AGND','AUX_5V']+[f'OP{n}_{p}' for p in ['INP','INN','OUT']]
    a.append(f'(sheet (at {x} {y}) (size {w} {h}) (stroke (width 0.254) (type default)) (fill (color 0 0 0 0)) (uuid "{su}") '+prop('Sheetname',f'Channel {n}',x,y-2.54)+prop('Sheetfile',f'opamp_ch{n}.kicad_sch',x,y+h+2.54)+'\n'+'\n'.join(f'(pin "{p}" passive (at {x} {y+12.7+i*12.7} 180) {fx(1.27,"left")} (uuid "{uid()}"))' for i,p in enumerate(ports))+f'(instances (project "opamp_block" (path "/{root}" (page "{n+1}")))))')
    for i,p in enumerate(ports):
        py=y+12.7+i*12.7;a.extend([wire((x,py),(x-12.7,py)),label(p,x-12.7,py)])
a.append(txt('INTEGRATION / BUILD NOTES\n- Master owns chip, bench VAA entry/current break, scan header and AGND/DGND tie.\n- AUX_5V enters at J_AUX; its bench return connects to the board AGND.\n- No global labels: child supplies and signals pass through sheet pins.\n- Keep all three schematic files together; footprints are intentionally empty.\n- Pin 48: OPAMP1 block label vs op2_inp signal name remains unresolved.\n- REF feedback is sensed after R_REFISO; C_REF2A is DNP pending stability review.',15.24,320.04,1.7))
a.append(f'(sheet_instances (path "/" (page "1"))))');(OUT/'opamp_block.kicad_sch').write_text('\n'.join(a))
for n,su in enumerate(childids,1):
    gg=groups[1:] if n==1 else [[{**c,'ref':ch2(c['ref'])} for c in g] for g in groups[1:]]
    a=sheetstart(uid(),f'Channel {n} | fixtures A, B, C and D',set(c['type'] for g in gg for c in g))
    a.append(txt(f'CHANNEL {n}  /  FIT ONE FIXTURE\'S THREE ISOLATION SHUNTS AT A TIME',15.24,17.78,2.54))
    for i,p in enumerate(['REF','AGND','AUX_5V']+[f'OP{n}_{p}' for p in ['INP','INN','OUT']]):
        x=35.56+i*91.44;a.extend([hlabel(p,x,27.94),wire((x,27.94),(x+15.24,27.94)),label(p,x+15.24,27.94)])
    titles=['A / Vos, Ib, Ios','B / Slew rate, phase margin, GBW, PD/Iq','C / Open-loop gain and output swing','D / Output impedance - ALL DNP']
    notes=[f'Guard CH{n}_A_SUM, CH{n}_A_INN, CH{n}_A_NIP, CH{n}_A_INP with REF.\nNo vias inside guard; no solder-mask opening. Switches independent.',f'JP{n}_BG open: follower; closed: gain ~101. DC coupling default.\nAC option: remove R{n}_BDIR; fit C{n}_BAC and R{n}_BBIAS.',f'JP{n}_C closed for retained tests. Servo feedback passes through chip.\nR{n}_CVC fitted at 0 ohm; C{n}_CNULL DNP. Do not add local feedback.',f'All symbols retained with DNP flags. Values await AD / ZO / frequency.\nCoax shield returns to AGND; stimulus referenced/offset to REF.']
    for gi,g in enumerate(gg):
        bx=15.24+(gi%2)*284.48;by=43.18+(gi//2)*172.72
        a.append(txt(titles[gi],bx,by,2.0))
        for i,c in enumerate(g):a.append(comp(c,bx+30.48+(i%3)*91.44,by+22.86+(i//3)*27.94,'/'+root+'/'+su))
        a.append(txt(notes[gi],bx,by+153.67,1.1))
    a.append(txt('BUILD: silkscreen fixture letters beside isolation jumpers. TBD and TBD-AD are intentional. No PCB placement/routing.\nFixture B PD/Iq is an EDU1 engineering adaptation, not literal Figure 4005-1 conformity.',15.24,392.43,1.15))
    a.append(')');(OUT/f'opamp_ch{n}.kicad_sch').write_text('\n'.join(a))
(OUT/'opamp_block.kicad_pro').write_text(json.dumps({'meta':{'filename':'opamp_block.kicad_pro','version':1},'net_settings':{'classes':[{'name':'Default','clearance':0.2,'track_width':0.25,'via_diameter':0.6,'via_drill':0.3}],'meta':{'version':3}},'schematic':{'annotate_start_num':0}},indent=2)+'\n')
(OUT/'expected_v4.json').write_text(json.dumps({'components':cs,'nets':nets,'external':ext,'symbol_pin_maps':{t:{p[0]:p[1] for p in pp} for t,pp in pins.items()}},indent=2))
print('Generated from v4: 12 + 53 + 53 components; 6 + 29 + 29 nets; 8 external labels.')
