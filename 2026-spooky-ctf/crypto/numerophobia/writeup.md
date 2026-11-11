# Numerophobia — Writeup

**Flag:** `spooky{th3_4n5w3r_h45_4lw4y5_b33n_42}`

**Category:** Crypto / encoding (character codes with an alternating shift, reversed)

**Files:** `numerophobia.txt` (367 bytes, one line, 116 space-separated integers)

---

## 1. The story is the key

The challenge text has three clues that matter. Each one describes one step:

| Clue | Meaning |
|---|---|
| "screaming **random numbers**" | each number is the decimal code of one character |
| "**every other step** was missing and marked with a **13**" | every other number has been shifted by 13 |
| "a book about **dyslexia**" | the text is reversed |

## 2. Recon

```
23 50 65 50 65 50 65 ... 50 65 10 138 50 65 95 123 51 64 98 108 53 134 ...
... 10 63 52 63 52 63 52 ... 63 52
```

Decoding the numbers directly as ASCII doesn't work:

- `23` is a control character.
- Values such as `138`, `134` and `132` fall outside printable ASCII.
- The plain `10`s (newline) and the long runs of repeated pairs (`50 65`, `63 52`)
  look like structure: a top border, a payload line and a bottom border.

The out-of-range values all sit at **even indices**, so those are the numbers that
were shifted.

## 3. Undo the shift

Subtract 13 from every number at an even index (counting from 0) and leave the
odd-index numbers alone:

```
23  -> 10  '\n'      50 -> '2' (unchanged)      65 -> 52  '4'
138 -> 125 '}'       95 -> '_' (unchanged)      123 -> 110 'n'
63  -> 50  '2'       52 -> '4' (unchanged)
```

Every value now lands in printable ASCII (or newline), which confirms the even
indices were the shifted ones. The output:

```

24242424242424242424242424242424242424
}24_n33b_5y4wl4_54h_r3w5n4_3ht{ykoops
24242424242424242424242424242424242424
```

> The "13" is not ROT13. Applying ROT13 to letters gets nowhere. It's a plain
> arithmetic shift of the character code.

## 4. Reverse it

`}...{ykoops` is `spooky{...}` written backwards, which is the dyslexia clue.
Reversing the whole string gives:

```
42424242424242424242424242424242424242
spooky{th3_4n5w3r_h45_4lw4y5_b33n_42}
42424242424242424242424242424242424242
```

The borders become rows of `42`, and the flag spells out *"the answer has
always been 42"*, a Hitchhiker's Guide reference that fits the man screaming
numbers.

## 5. Solver

`solve.py`:

```python
import sys
nums = list(map(int, open(sys.argv[1] if len(sys.argv) > 1 else "numerophobia.txt").read().split()))
# every other number (even indices) had 13 added; undo it
chars = [chr(n - 13 if i % 2 == 0 else n) for i, n in enumerate(nums)]
print("".join(chars)[::-1])  # dyslexia: read it backwards
```

```console
$ python3 solve.py numerophobia.txt
42424242424242424242424242424242424242
spooky{th3_4n5w3r_h45_4lw4y5_b33n_42}
42424242424242424242424242424242424242
```

**Flag:** `spooky{th3_4n5w3r_h45_4lw4y5_b33n_42}`
