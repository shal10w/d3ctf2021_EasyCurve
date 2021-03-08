from sage.all import *
from pwn import *
from Curve import MyCurve
from pwnlib.util.iters import mbruteforce
import string
from hashlib import sha256
from Crypto.Util.number import *
#context.log_level = 'debug'
port = 10000
ip = '47.100.50.252'
io = remote(ip , port)
p = 9688074905643914060390149833064012354277254244638141162997888145741631958242340092013958501673928921327767591959476890238698855704376126231923819603296257
R = GF(p)
def proof_of_work(p):
    p.recvuntil("XXXX+")
    suffix = p.recv(16).decode("utf8")
    p.recvuntil("== ")
    cipher = p.recvline().strip().decode("utf8")
    proof = mbruteforce(lambda x: sha256((x + suffix).encode()).hexdigest() ==
                        cipher, string.ascii_letters + string.digits, length=4, method='fixed')
    p.sendlineafter("Give me XXXX: ", proof) 


def hackOT(d):
    io.recvuntil('n = ')
    n = int(io.recvline()[:-1])
    io.recvuntil('e = ')
    e = int(io.recvline()[:-1])
    io.recvuntil('x0 = ')
    x0 = int(io.recvline()[:-1])
    io.recvuntil('x1 = ')
    x1 = int(io.recvline()[:-1])
    v = (x0 + pow(-d , e, n) * x1) * inverse(1 + pow(-d , e , n) , n) % n
    io.sendline(str(v))
    io.recvuntil("m0_ = ")
    m0_ = int(io.recvline()[:-1])
    io.recvuntil("m1_ = ")
    m1_ = int(io.recvline()[:-1])
    res = (m0_ - d * m1_) % n - n
    return R(res)
def getd():
    io.recvuntil('D = ')
    D = R(int(io.recvline()[:-1]))
    if pow(D , (p-1)//2 , p) != 1:
        return -1
    else:
        d = int(D.sqrt(0))
        assert pow(d ,2 , p) == D
        return d   


while 1:
    proof_of_work(io)
    d = getd()
    if d == -1:
        io.close()
        io = remote(ip , port)
        continue
    a1 = hackOT(d)
    a2 = hackOT(d)
    io.recvuntil("do you know my e?")
    io.sendline('0')
    io.recvuntil("I know you can't get it.")
    b1 = hackOT(d)
    b2 = hackOT(d)
    e = discrete_log(b2/a2,b1 / a1)
    print(e)
    io.recvuntil("do you know my e?")
    io.sendline(str(e))
    io.interactive()
    break