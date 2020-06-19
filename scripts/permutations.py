#-*- coding:utf-8 -*-
def permutations(inp: str = 'abc', out: str = ''):
    """Перестановки строки"""
    if len(inp) == 0:
        print(out)
    for i in range(len(inp)):
        sub = inp[0:i] + inp[i+1:]
        tmp = out + inp[i]
        permutations(sub, tmp)

permutations()
permutations('1234') # 1*2*3*4=24