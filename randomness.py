 ##pzc
##2013-12-2
##rabbitpzc@gmail.com

import random
import numpy as np
import copy

def neighbor(v):
    i, j = v
    return ((N+i-1)%N, j), ((N+i+1)%N, j), (i, (N+j-1)%N), (i, (N+j+1)%N)

def init_network(N):
    Net = {}
    for i in xrange(N):
        for j in xrange(N):
            Net[(i, j)] = {'base':set([]), 'inter':()}
    return Net

def network(N, c):
    G = init_network(N)
    D = init_network(N)

    rlist1 = []
    for i in xrange(N):
        for j in xrange(N):
            if random.random() < c:
                rlist1.append((i, j))
    rlist2 = copy.deepcopy(rlist1)
##    random.shuffle(rlist1)
    random.shuffle(rlist2)
    random.shuffle(rlist2)
    random.shuffle(rlist2)
    rdict = dict([(rlist1[x], rlist2[x]) for x in xrange(len(rlist1))])
    for i in xrange(N):
        for j in xrange(N):
            G[(i, j)]['base'] = set(neighbor((i, j)))
            D[(i, j)]['base'] = set(neighbor((i, j)))
            if (i, j) in rdict:
                G[(i, j)]['inter']=rdict[(i, j)]
                D[rdict[(i, j)]]['inter']=(i, j)
            else:
                G[(i, j)]['inter']=(i, j)
                D[(i, j)]['inter']=(i, j)
       
    return G, D

def gaint_component(GG):
    CC = {}
    c = 0
    for v in GG:
        if v in CC:
            continue
        c += 1
        CC[v] = c
        neighbor_node = [v]
        while len(neighbor_node) > 0:
            top = neighbor_node.pop()
            CC[top] = c
            for node in GG[top]['base']:
                if node not in CC:
                    CC[node] = c
                    neighbor_node.append(node)
    count={}
    for v in CC:
        count.setdefault(CC[v], 0)
        count[CC[v]] += 1
    if len(count) == 0:
        return [], 0, 0
    else:
        cnt = max(count.values())
        return CC, count.keys()[count.values().index(cnt)], cnt

def update_base(GG, DD, v, inter_target):
    for s in neighbor(v):
        if s not in GG:
            continue
        GG[s]['base'] = GG[s]['base'] - set([v])
        if len(GG[s]['base']) <= 0:
            if GG[s]['inter'] in DD:
                inter_target.append(GG[s]['inter'])
            del GG[s]
    return inter_target

def destroy_base(GG, DD, target, inter_target):
    for v in target:
        if v not in GG:
            continue
        inter_target = update_base(GG, DD, v, inter_target)
        if GG[v]['inter'] in DD:
            inter_target.append(GG[v]['inter'])
        del GG[v]
    return inter_target
    
def destroy(G, D, target): 
    GG, DD = G, D
    flag = True
    niter = 0
    while len(target)!=0:
        niter += 1
        #destory target initially given
        inter_target = []
        destroy_base(GG, DD, target, inter_target)

        #destroy target not in the gaint component
        base_target = []
        CC, idx, cnt = gaint_component(GG)
        for v in CC:
            if CC[v] != idx:
                base_target.append(v)
        destroy_base(GG, DD, base_target, inter_target)

        #change inter target to base target
        #and switch inter and base network
        target = inter_target        
        DD, GG = GG, DD

##        #clear isolate node, not really used...
        clear_isolate_node(G)
        clear_isolate_node(D)
    return niter

def clear_isolate_node(GG):
    for i in GG.keys():
        if len(GG[i]['base']) <= 0 or len(GG[i]['inter']) <= 0:
            del GG[i]
            
def random_destroy(G, D, p):
    n = 0
    target = []
    for t in G.keys():
        if random.random() < p:
            n += 1
            target.append(t)
            
    return destroy(G, D, target)        
            

pp={}
target = []
N = 100
for c in np.arange(0.0, 1.1, 0.1):
    for p in np.arange(0.01, 1.01, 0.01):
        G, D = network(N, c)
        niter = random_destroy(G, D, p)
        pp.setdefault(p, {})
        CC, idx, cnt = gaint_component(G)
        pp[p][c] = cnt
        
        print c, p, cnt, niter
##        if len(G) == 0:
##            print c, p
##            break
##        
fout=open('out.dat', 'w')
label = '\t'.join(map(str, pp[pp.keys()[0]].keys()))
fout.write('\t'.join(['0.00', label]) + '\n')
for p in pp:
    value = '\t'.join(map(str, pp[p].values()))
    fout.write('\t'.join([str(p), value]) + '\n')
fout.close()




