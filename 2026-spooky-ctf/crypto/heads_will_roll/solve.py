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
