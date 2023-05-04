from cmath import inf
import numpy as np
import matplotlib.pyplot as plt
import sys
import itertools
import math
import rulelist as m3

NUM_RULES = 2
INPUT_SIZE = 8
OUTPUT_SIZE = 8
 
def decimalToBinary(n):
    return "{0:09b}".format(int(n))


def BinaryTodecimal(bit_list):
    dec = 0
    for bit in bit_list:
        dec = (dec << 1) | bit
    return dec


def rule_op(rule, nb_size, ca_len, ca, start):
    ops = []
    for i in range(start, start+ca_len-nb_size+1):
        nbr = []
        for j in range(nb_size):
            nbr.append(ca[(i+j) % ca_len])
        ops.append(rule(nbr))
    res = 0
    for op in ops:
        res ^= op
    return res


rule_list, rule_names = m3.return_rules()


def Sbox(rules):
    inputs = []
    outputs = []

    for i in range(2**INPUT_SIZE):
        res = list(map(int, str(decimalToBinary(i))))
        res = res[1:]
        inputs.append(res)
        op = []
        start = 0
        for rule in rules:
            for i in range(math.ceil(INPUT_SIZE/NUM_RULES)):

                op.append(rule_op(rule, 3, INPUT_SIZE, res, start))
                start += 1
        op = op[0:8]
        outputs.append(op)
    return inputs, outputs

def bijectivity(decimal_repr):
    len_ops = len(decimal_repr)
    len_distinct = len(set(decimal_repr))
    if (len_ops == len_distinct):
        print("It is Bijective")
        return 1
    else:
        print("Not Bijective")
        return 0

def diff_uniformity(decimal_repr):
    ddt = np.zeros((2**INPUT_SIZE, 2**INPUT_SIZE))
    for a in range(2**INPUT_SIZE):
        for x in range(2**INPUT_SIZE):
            sum = x ^ a
            F1 = decimal_repr[sum]
            F2 = decimal_repr[x]
            b = F1 ^ F2
            ddt[a][b] += 1
    # for i in range(2**INPUT_SIZE):
    #     ddt[i][i] = 0
    ddt[0] = np.zeros(2**INPUT_SIZE)
    return (np.amax(ddt))


def innerprod(a, x):
    res = 0
    if (len(x) != len(a)):
        print(f"SIZE a={len(a)} SIZE x={len(x)}")
    for i in range(len(a)):
        res ^= ((a[i]*x[i]) % 2)
    return res

def WHT_Calc(u, v, inarray, outarray):
    WHT = 0
    for i in range(len(inarray)):
        x = innerprod(v, outarray[i])
        y = innerprod(u, inarray[i])
        WHT += pow(-1, x ^ y)
    return WHT

def get_WHT_spectrum(inarray, outarray):
    v_vals = list(itertools.product([0, 1], repeat=OUTPUT_SIZE))
    u_vals = list(itertools.product([0, 1], repeat=INPUT_SIZE))
    v_vals = v_vals[1:]
    max = -inf
    for u in u_vals:
        for v in v_vals:
            WHT_curr = abs(WHT_Calc(u, v, inarray, outarray))
            if (WHT_curr > max):
                max = WHT_curr
    return max

def NLcalc(inarray, outarray, n):
    wht = get_WHT_spectrum(inarray, outarray)
    NL = pow(2, n-1) - wht/2
    return NL

def fitness(rules_index, to_print):

    rules = [rule_list[i] for i in rules_index]
    inarray, outarray = Sbox(rules)
    decimal_repr = []
    for bit_list in outarray:
        decimal_repr.append(BinaryTodecimal(bit_list))
    DU = diff_uniformity(decimal_repr)
    NL = NLcalc(inarray, outarray, INPUT_SIZE)

    normalised_NL = (NL/112)*100
    DU1 = ((DU-4)/(128-4))*100
    normalised_DU = 100 - DU1
    reward = (normalised_NL + normalised_DU)/2
    if to_print:
        print(f"DU = {str(DU)} NL={str(NL)}")
        print(f"Strength: {round(reward,2)}")

    return reward, DU, NL