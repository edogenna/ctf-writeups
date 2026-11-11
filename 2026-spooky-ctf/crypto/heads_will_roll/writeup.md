# Pumpkin Head — Writeup

**Flag:** `spooky{5l33py_h0ll0w_h34d5}`

**Category:** Crypto (classical / rail fence transposition)

**Files:** `pumpkin_head_message.txt` (68 bytes, one line, no newline)

---

## 1. Reading the riddle

> While **rolling, rolling, rolling, rolling**, through the air, his pumpkin head
> shouted… what? His perfect aim knocked Ichabod to the ground **near the rails**…

- **"near the rails"** points to a **rail fence cipher**.
- **"rolling" ×4** gives the key: **4 rails**.

## 2. Recon

```
Etu_taip5_w5n_hpmnw_hlgsdso{lyh0_d}jyi_piihef_ne_oy3p0lh4oskt_i:k3l3
```

- Plain printable ASCII. There's no encoding layer to strip (`xxd` shows nothing hidden).
- `{`, `}`, `_` and the leetspeak digits are present, but the letters are in the
  wrong order. `s p o o k y` shows up scattered rather than together.
- That fits a **transposition**: the characters are right but their positions
  are shuffled. A substitution cipher would have changed the characters themselves.

## 3. How a 4-rail fence works

Plaintext is written in a zigzag across 4 rows (rails), and the ciphertext is the
rows read left to right, top to bottom. The zigzag repeats every `2·(4−1) = 6`
characters. Here are the first 24 characters of the plaintext:

```
rail 0: E.....t.....u....._.....
rail 1: .n..._.h...p.m...n.w..._
rail 2: ..j.y...i._...p.i...i.h.
rail 3: ...o.....s.....k.....t..
```

With 68 characters the rails hold 12, 23, 22 and 11 characters, so the
ciphertext splits as:

```
rail 0 (12): Etu_taip5_w5
rail 1 (23): n_hpmnw_hlgsdso{lyh0_d}
rail 2 (22): jyi_piihef_ne_oy3p0lh4
rail 3 (11): oskt_i:k3l3
```

To decrypt, work out which rail each plaintext position belongs to, sort the
positions by (rail, index), and deal the ciphertext characters back into them in
that order.

## 4. Brute force as confirmation

The riddle already gives 4 rails. To rule out a lucky misreading, I tried every
rail count from 2 to 19 and every starting offset. Only **4 rails, offset 0**
gives readable text from start to finish:

```
4 0 Enjoy_this_pumpkin_with_the_flag_inside:_spooky{5l33py_h0ll0w_h34d5}
```

The other hits for 4 rails (offsets 2 and 4) are the same sentence rotated, and
nothing for 3, 5 or 6 rails is readable. For example:

```
3 0 En3wt_phul0g_sldtshoa{4liyohp0s_5dk}_jtywi__5piini:h_ekfh_3npel_mo3y
5 0 E_oetf{wt5l__nynu_hei_0h_p_o:ydmtn}3kpjwa_y03lihil_hl4pgpsio3sid5shk
```

## 5. Solver

`solve.py`:

```python
import sys
def rail_decrypt(ct, rails):
    cyc = 2 * (rails - 1)
    rail_of = [min(i % cyc, cyc - i % cyc) for i in range(len(ct))]
    order = sorted(range(len(ct)), key=lambda i: (rail_of[i], i))
    out = [""] * len(ct)
    for ch, pos in zip(ct, order):
        out[pos] = ch
    return "".join(out)
ct = open(sys.argv[1] if len(sys.argv) > 1 else "pumpkin_head_message.txt").read().strip()
print(rail_decrypt(ct, 4))
```

```console
$ python3 solve.py pumpkin_head_message.txt
Enjoy_this_pumpkin_with_the_flag_inside:_spooky{5l33py_h0ll0w_h34d5}
```

The pumpkin head shouted: *"Enjoy this pumpkin with the flag inside:
spooky{5l33py_h0ll0w_h34d5}"*, which is "sleepy hollow heads" in leetspeak.

**Flag:** `spooky{5l33py_h0ll0w_h34d5}`
