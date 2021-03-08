# d3ctf2021_EasyCurve

题中曲线为由pell方程构造的曲线
但参数没给全，只给了D，没给u。同时OT也不允许用户同时拿到x和y算出u(预期是这么想的，但后来发现没考虑全面，选手仍然能够同时拿到x与y)
研究曲线，加法规则是用斜率写的，经过一番计算可以将其换成关于点坐标的式子
A(x1,y1) + B(x2 , y2) = C(x3,y3)
则其坐标之间满足
x3 = (x1x2 + Dy1y2)\*inverse(u , p) % p
y3 = (x1y2 + x2y1)\*inverse(u , p) % p
可以推出当D与u为二次剩余时，曲线上的点与GF(p)有一个映射
(x , y) -> a(x - dy)  (其中a\^2 = u,d\^2 = D)
k(x , y) -> [a(x - dy)]\^k

（关于这个映射详细可见paper《A PUBLIC KEY CRYPTOSYSTEM BASED ON PELL EQUATION》这里对它进行了一点小修改，具体思路类似）

通过这个映射能够将曲线上的dlp问题转化为模p的dlp问题。
同时，题中实现的OT虽然不能同时得到x与y，但是可以通过构造v = (x0 + pow(-d , e, n) * x1) * inverse(1 + pow(-d , e , n) , n) % n
来让m0 - d * m1 = x - dy
因此我们可以得到若A = eG
则(X_a - dY_a)  = a^(e-1) \* (X_g - dY_g)^e
里面还有未知数a，但题目给了三组数据，因此我们可以用两组数据相除来消去a。最后将题目转化为mod p的dlp问题，而将p-1分解可发现p-1很光滑，可以轻松计算出e
不过这题也出了非预期，由于x和y均过小，若OT取d 大于x和y，模d后可以得到x，减去x后除以可以得到y，得到u后，接着可以直接在曲线上计算dlp。（思路源自天枢与redbud的wp）

具体代码在exp.py中