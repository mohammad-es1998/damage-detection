import math
from ctypes import c_float

from darknet import *

from app.ai.darknet_lib.darknet import c_array, predict, reset_rnn, load_net, sample


def predict_tactic(net, s):
    prob = 0
    d = c_array(c_float, [0.0] * 256)
    tac = ''
    if not len(s):
        s = '\n'
    for c in s[:-1]:
        d[ord(c)] = 1
        pred = predict(net, d)
        d[ord(c)] = 0
    c = s[-1]
    while 1:
        d[ord(c)] = 1
        pred = predict(net, d)
        d[ord(c)] = 0
        pred = [pred[i] for i in range(256)]
        ind = sample(pred)
        c = chr(ind)
        prob += math.log(pred[ind])
        if len(tac) and tac[-1] == '.':
            break
        tac = tac + c
    return tac, prob


def predict_tactics(net, s, n):
    tacs = []
    for i in range(n):
        reset_rnn(net)
        tacs.append(predict_tactic(net, s))
    tacs = sorted(tacs, key=lambda x: -x[1])
    return tacs


net = load_net("cfg/coq.test.cfg", "/home/pjreddie/backup/coq.backup", 0)
t = predict_tactics(net, "+++++\n", 10)
print(t)
