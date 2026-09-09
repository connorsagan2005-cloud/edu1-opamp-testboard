import re,json
class Q(str): pass
def parse(s):
    tokens=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',s); stack=[]; root=None
    for t in tokens:
        if t=='(':
            a=[]
            if stack: stack[-1].append(a)
            else: root=a
            stack.append(a)
        elif t==')': stack.pop()
        else: stack[-1].append(Q(json.loads(t)) if t.startswith('"') else t)
    assert not stack
    return root
def dump(a):
    if isinstance(a,list): return '('+' '.join(map(dump,a))+')'
    if isinstance(a,Q): return json.dumps(str(a),ensure_ascii=False)
    return str(a)
def children(a,k): return [x for x in a if isinstance(x,list) and x and x[0]==k]
def one(a,k): return next(x for x in a if isinstance(x,list) and x and x[0]==k)
