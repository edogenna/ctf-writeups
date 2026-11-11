# "There is no good name for the fear of math" — Writeup

**Category:** Cryptography
**Technique:** Class-function key recovery against a conjugacy-based (non-associative) Diffie–Hellman
**Flag:** `spooky_scary_nonassociative_diffie_hellman`

---

## Challenge

We're given `chal.py` only — no server. It defines a group of 4-tuples
`(a, b, c, d)` (first coordinate mod `p`, the rest mod `q`), a multiplication
`mul`, an inverse `inv`, conjugation `conj(x, g) = inv(x)·g·x`, and a key-exchange:

```python
Ma, Mb = conj(a, g), conj(b, g)          # public
K = shared_key(a, g, Mb)                 # = assoc(a, g, Mb) * mu^(-a[0])
ct = bytes(x ^ y for x, y in zip(flag, mask(K, 42))).hex()
```

Public data: `g`, `Ma`, `Mb`, `ct`. Secrets `a`, `b`, `flag` are `None` in the file
(they were filled in when the challenge was generated). We must recover `K`.

### Parameters
```
p  = 1099511640127                                  # prime
q  = 340282370743387819766807672197819448083        # 129-bit prime
mu = 145131588818725534535896278189401302887
```
`p` is prime and `p | q − 1`, so `mu` has order `p` in `(Z/q)*` — hence
`mpow(e) = mu^(e mod p) mod q` is well defined.

## The group

Projecting away the `d` coordinate, an element is `(a0, b, c) ∈ Z/p × Z/q × Z/q`
and the product is

```
(a1,b1,c1)·(a2,b2,c2) = ( a1+a2 ,  b1·mu^(-a2)+b2 ,  c1·mu^(-a2)+c2 )
```

i.e. `Z/p` acts on `(Z/q)^2` by scaling by `mu^(-a)` (a metabelian group); `d` is a
central quadratic cocycle. The scheme is a conjugacy-search ("non-commutative DH"):
security is *supposed* to rest on recovering `a` from `Ma = conj(a, g)`.

## Key observations

**1. `assoc` ignores `d`.** The associator form only reads the first three
coordinates of each argument:

```python
def assoc(x, y, z):
    ax,bx,gx,_ = x; ay,by,gy,_ = y; az,bz,gz,_ = z
    ...
```

So `K = shared_key(a, g, Mb)` depends on `a` only through `(a0, b_a, c_a)`.

**2. Conjugation on the projection is linear and under-determined.**
Writing `a = (a0, B, C)`, `g = (g0, gb, gc)` and pushing `conj` through the
coordinate formulas gives:

```
Ma_b = B·(1 − mu^(-g0)) + gb·mu^(-a0)
Ma_c = C·(1 − mu^(-g0)) + gc·mu^(-a0)
```

Two equations, three unknowns (`B`, `C`, and `a0` via `t = mu^(-a0)`). For **any**
chosen `a0`, we can solve for a consistent `(B, C)` with
`D = (1 − mu^(-g0))`:

```
B = (Ma_b − gb·t) · D^(-1) mod q
C = (Ma_c − gc·t) · D^(-1) mod q
```

**3. The shared key is a class function.** Substituting those reconstructed
`(B, C)` into `shared_key` and evaluating for several `a0` values gives the **same
`K` every time**:

```
a0=0            K=286324188360977795495506529564082791425
a0=1            K=286324188360977795495506529564082791425
a0=12345        K=286324188360977795495506529564082791425
a0=999999999    K=286324188360977795495506529564082791425
```

So the secret first coordinate and `d` are irrelevant — we never needed to solve
the conjugacy-search problem at all. We just pick a convenient representative
(`a0 = 0`) of the conjugating coset and read off `K`.

## Exploit

```python
import hashlib
p  = 1099511640127
q  = 340282370743387819766807672197819448083
mu = 145131588818725534535896278189401302887
phi = (-2 * pow(mu - 1, -1, q)) % q
inv_mu = pow(mu - 1, -1, q)
g  = (739614761553, 87671554642066775345573935247301052006,
      85147831812679793672994902968842668105, 71719252422814786229685092573269912498)
Ma = (739614761553, 312134278234991743315140578529310805510,
      126369916264124511285906038626254340804, 134610391672392132751140546119763556201)
Mb = (739614761553, 244699321175961590059239024660541174646,
      335110553885376877685776857080059519613, 55552870219389410159628089275413443533)
ct = bytes.fromhex("9915497c4929fceea2ab3cfd06a744ac9ff6d8de290c8911d18b746d885fb3f5508282d2da0adff5fa15")

def mpow(e): return pow(mu, e % p, q)
def assoc(x, y, z):
    ax,bx,gx,_ = x; ay,by,gy,_ = y; az,bz,gz,_ = z
    t1 = mpow(ax+ay)*(mpow(az)-1)*(bx*gy - by*gx)
    t2 = mpow(ay+az)*(mpow(ax)-1)*(by*gz - bz*gy)
    t3 = mpow(az+ax)*(mpow(ay)-1)*(bz*gx - bx*gz)
    return (t1+t2+t3)*inv_mu % q
def shared_key(a, g, Mb): return assoc(a, g, Mb) * mpow(-a[0]) % q
def mask(K, n): return hashlib.shake_256(b"loop|" + K.to_bytes(32,"big")).digest(n)

g0, gb, gc = g[0], g[1], g[2]
D = (1 - mpow(-g0)) % q
Dinv = pow(D, -1, q)

def reconstruct(M, a0=0):
    t = mpow(-a0)
    B = (M[1] - gb*t) * Dinv % q
    C = (M[2] - gc*t) * Dinv % q
    return (a0 % p, B, C, 0)

a_rec = reconstruct(Ma, 0)                 # any a0 works
K = shared_key(a_rec, g, Mb)
flag = bytes(x ^ y for x, y in zip(ct, mask(K, len(ct))))
print(flag.decode())
```

### Output
```
K    = 286324188360977795495506529564082791425
flag = spooky_scary_nonassociative_diffie_hellman
```

## Notes

- The encryptor's key is `shared_key(a, g, Mb)`, so the **a-side** reconstruction is
  the one that matches. Reconstructing `b` from `Mb` and computing
  `shared_key(b, g, Ma)` does **not** give the same value (`K1 != K2`) — the `assoc`
  form isn't symmetric between the two parties, which is the "non-associative" joke
  the flag refers to. We only ever needed the a-side.
- No network interaction required; this is a fully offline recovery.

## Root cause / lesson

The protocol tries to hide a secret in the conjugating element, but the derived key
is constant across the entire coset of elements that conjugate `g` to `Ma`
(a centralizer coset). Any such representative — trivially `a0 = 0` — reproduces the
key, so the conjugacy-search "hard problem" is bypassed by solving a small linear
system mod `q`. A key-exchange value must not be a class function of public data.
