import re

# a = """.fa-glass:before{content:"\f000"}
# ... .fa-music:before{content:"\f001"}
# ...
# arr = a.split('\n')

rega_fa = re.compile('\.fa-[a-z-]*)', re.I+re.U+re.DOTALL)

def calc():
    for item in arr:
        res = rega_fa.search(item)
        if res:
            print('        {"id": "%s", "text": "%s"},' % (res.group(1), res.group(1)))
        else:
            pass