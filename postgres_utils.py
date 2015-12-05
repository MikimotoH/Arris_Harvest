# coding: utf-8
from collections import OrderedDict
import re


def dict2hstore(dic:dict)->str:
    """
    postgresql uese 'backslash' to escape double quote inside double quote
    GridIot=# select 'a=>"hello\"world"'::hstore -> 'a';
      ?column?   
      -------------
       hello"world
       (1 row)
    """
    def escapeDQuote(s):
        return re.sub(r'(?<!\\)"', '\\"', str(s))
    def sdq(s):
        return '"'+escapeDQuote(s)+'"'
    return ', '.join(sdq(k)+"=>"+sdq(v) for k,v in dic.items())

def hstore2dict(hstore:str)->dict:
    """
    hstore='"DMZ"=>"true", "QoS"=>"true", "RAM"=>"512 Mb"'
    """
    def unescapeDQuote(s):
        return re.sub(r'\\"', '"', s)
    dic = OrderedDict()
    i = 0
    while True:
        m = re.search(r'"(.+?)(?<!\\)"=>"(.+?)(?<!\\)"', hstore[i:])
        if not m:
            break
        kname = m.group(1); vname = m.group(2)
        dic[unescapeDQuote(kname)] = unescapeDQuote(vname)
        i = i + m.span()[1] 
        if hstore[i:i+2] != ', ':
            break
        i = i+2
    return dic

