import random
import base64
import sys
import os

def split_string(s, x):
    return [s[i:i+x] for i in range(0, len(s), x)]

def get_val(ar,val):
    x=0
    for i in ar:
        if i == val:
            x=1
        elif x == 1:
            return i 

def key(text):
    x = 0
    y = 0
    rep=0
    for i in text:
        x+=ord(i)
        y+=ord(i)*(10^rep)
        rep+=1
    return x*y

def substitution(input,key):
    dict={}
    vals=[]
    random.seed(key)
    for i in range(256):
        dict[i]=i
    vals = list(range(256))
    random.shuffle(vals)
    num=0
    for i in dict:
        dict[i]=vals[num]
        num+=1
    output=b""
    for i in input:
        output=output+bytes([dict[i]])
    return output

def subs_d(input,key):
    dict={}
    vals=[]
    random.seed(key)
    for i in range(256):
        dict[i]=i
    vals = list(range(256))
    random.shuffle(vals)
    num=0
    for i in dict:
        dict[i]=vals[num]
        num+=1
    output=b""
    dict_val = {v: k for k, v in dict.items()}
    for i in input:
        output=output+bytes([dict_val[i]])
    return output

def getbytes(key,lenght):
    key = key.encode("utf-8")
    return bytes(key[i%len(key)] for i in range(lenght))

def xor(text):
    global seedtxt
    key=b""
    out=b""
    key = getbytes(seedtxt,len(text))
    out = bytes(a ^ b for a, b in zip(text, key))
    return out

def divide(text,seed):
    num=int((str(seed))[0])
    arr=split_string(text,num)
    out=b""
    for j in arr:
        out+=bytes(reversed(j))
    return out 

def encrypt(text,seed):
    out=text
    out = substitution(out,seed)
    if int(str(seed)[0])%2==0:
        out = divide(out,seed)
    out = xor(out)
    return base64.b64encode(out).decode("utf-8")

def decrypt(text,seed):
    out=base64.b64decode(text)
    out=xor(out)
    if int(str(seed)[0])%2==0:
        out = divide(out,seed)
    out = subs_d(out,seed)
    return out

decode=False

helptext=["Arguments:","    -d: decode instead of encrypt","    -i: input file","    -o: output file","    -k: key","    -h: display this list ;)"]
args = sys.argv
text=""
del args[0]
if "-h" in args:
    for i in helptext:
        print(i)
    exit()
if args == []:
    print("No arguments were added!")
    for i in helptext:
        print(i)
if "-i" in args:
    filein = get_val(args,"-i")
    if not "-d" in args:
        with open(filein,"rb") as d:
            text=d.read()
    else:
        with open(filein,"r") as d:
            text=d.read()

if "-k" in args:
    seedtxt=get_val(args,"-k")
else:
    seedtxt=input("Please enter key: ")
seed=key(seedtxt)
if text=="":
    if not "-d" in args:
        text=bytes(input("Please enter text: "),"utf-8")
    else:
        text=input("Please enter text: ")

if "-d" in args:
    if "-o" in args:
        filein = get_val(args,"-o")
        if not os.path.isfile(filein):
            open(filein,"x")
        with open(filein,"wb") as f:
            b=decrypt(text,seed)
            f.write(b)
    else:
        print(decrypt(text,seed).decode("utf-8"))
else:
    if "-o" in args:
        filein = get_val(args,"-o")
        if not os.path.isfile(filein):
            open(filein,"x")
        with open(filein,"w") as f:
            f.write(encrypt(text,seed))
    else:
        print(encrypt(text,seed))