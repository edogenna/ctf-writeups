# Graveyard — Writeup

**Flag:** `spooky{eyez_are_watching_me}`

**Category:** Crypto (classical / monoalphabetic substitution)

**Files:** `graveyard_letter.txt` (2013 bytes, CRLF line endings)

---

## 1. Recon

The challenge ships a single text file. First look:

```
Ypejpof Erpveaypj,

Pmpj odagp zlw rptf, D'mp tprf zlwj eiopagp. ...
```

Observations:

- Pure ASCII, no non-ASCII or zero-width characters.
- CRLF line endings; no trailing-whitespace stego (only one incidental trailing
  space, on line 9).
- Word shapes, apostrophes, punctuation and capitalization are all preserved.
  `D'mp` (4 chars, `X'YZ`) and `lt` / `fl` / `df` sit exactly where English
  `I've`, `of` / `to` / `it` would.

That structure rules out transposition and points at a **monoalphabetic
substitution cipher** with casing and punctuation left intact.

## 2. Cracking the alphabet

The salutation is the crib. A two-word greeting ending in a comma, with the
second word matching the pattern `A-l-e-x-a-n-d-e-r`:

```
Ypejpof Erpveaypj,   ->   Dearest Alexander,
```

That single line yields nine pairs immediately:

| cipher | plain |        | cipher | plain |
|:------:|:-----:|:------:|:------:|:-----:|
| `y`    | `d`   |        | `r`    | `l`   |
| `p`    | `e`   |        | `v`    | `x`   |
| `e`    | `a`   |        | `a`    | `n`   |
| `j`    | `r`   |        | `o`    | `s`   |
| `f`    | `t`   |        |        |       |

Propagating those through the body resolves the rest quickly — `fcp` → `the`
gives `c→h`, `zlw` → `you` gives `z→y, l→o, w→u`, `bwof` → `just` gives `b→j`,
`kwdgn` → `quick` gives `k→q, g→c, d→i`, and so on.

### The trap: verify the map is a bijection

My first table decoded the letter into fluent English, but it was **wrong**. It
contained:

- `o → s` **and** `s → s` (two cipher letters colliding on plaintext `s`)
- nothing mapping to plaintext `z`

A monoalphabetic substitution is a permutation of the alphabet, so a collision
is a contradiction — one of those two entries had to be wrong. Checking
frequency settles it: `o → s` is confirmed dozens of times (`odagp`→`since`,
`eiopagp`→`absence`, `bwof`→`just`), while ciphertext `s` occurs **exactly once
in the entire file**:

```console
$ grep -o 's' graveyard_letter.txt | wc -l
1
$ grep -n 's' graveyard_letter.txt
13:pzps ejp xefgcdau hp. Bwof jphphipj waypjogljpo daofpey lt oqegpo eay fl xjeq df gljjpgfrz.
```

So the correct entry is **`s → z`**, which completes the permutation, and that
single occurrence lands squarely inside the clue word. `pzps` is not `eyes` — it
is **`eyez`**.

This is the whole puzzle, and it is a nice one: the intended misspelling is
hidden behind the solver's (and an LLM's) reflex to autocorrect a near-miss into
a real English word. The clue sentence also starts in **lowercase** while every
other sentence in the letter is properly capitalized — the author flagging
"take this verbatim, it is not prose."

### Final key

```
cipher: a b c d e f g h i j k l m n o p q r s t u v w x y z
plain:  n j h i a t c m b r q o v k s e p l z f g x u w d y
```

## 3. Solve script

```python
#!/usr/bin/env python3
KEY = dict(zip("abcdefghijklmnopqrstuvwxyz",
               "njhiatcmbrqosvkzepl zfgxuwdy".replace(" ", "")))

text = open("graveyard_letter.txt", encoding="ascii").read()
out = "".join(
    KEY.get(c.lower(), c).upper() if c.isupper() else KEY.get(c, c)
    for c in text
)
print(out)
```

(Key string in plain `a..z` cipher order:
`n j h i a t c m b r q o v k s e p l z f g x u w d y`.)

## 4. Decoded letter

> Dearest Alexander,
>
> Ever since you left, I've felt your absence. But I've also felt the presence
> of another, though I don't know who it is. No matter where I go, there's this
> feeling that follows me. If I ever think it's gone, I'll get a sudden chill up
> my spine to remind me. But I never see them. If I turn to look, I'll only see
> quick flashes of hair or clothes, but they'll be gone by the time I round the
> corner.
>
> It started when I was in crowded areas, like at the mall we used to go to
> every weekend. The one where we would just walk around and windowshop for
> hours. You know it. Or at least you did. Then I started feeling it at work,
> but thought it was just the creepy posters they hang everywhere. Those things
> have always freaked me out, you know that. They mess with my dreams even
> though I should be used to them by now.
>
> But a week ago, I started feeling it at home. When I was cooking dinner for
> just me, watching Hallmark movies in your old living room, or walking Little
> Alex outside. She misses you by the way. She never liked me much, but she's
> always causing a racket now. She used to be so cute when you were around,
> even if she was always trying to nip me.
>
> It's gotten worse the last couple nights. I'll feel someone watching me while
> I'm trying to sleep, but I'm in our house all alone with the alarm on and
> every door and window locked and covered. You'd think I'm so paranoid if you
> were still here.
>
> I've tried to look for you, but it's like you disappeared. Everywhere you used
> to go to "get some air" is just missing you. There's only one place I haven't
> tried yet. I know you used to come visit your mother every Sunday, but I never
> wanted to overstep. But I've run out of options. I have nothing left here, so
> I'm going to leave. But I'll put a clue that should help you find me if you
> still care.
>
> **eyez are watching me. Just remember underscores instead of spaces and to
> wrap it correctly.**
>
> I hope you find me before they do.
>
> Sincerely,
>
> The One You Left Behind

## 5. Extracting the flag

The penultimate paragraph states the flag and its formatting rules outright:

| instruction | action |
|---|---|
| `eyez are watching me` | the flag text, verbatim, misspelling included |
| "underscores instead of spaces" | `eyez_are_watching_me` |
| "wrap it correctly" | apply the CTF's wrapper, `spooky{...}` |

```
spooky{eyez_are_watching_me}
```

The "one place I haven't tried yet" — the mother's grave — is the narrative
payoff for the challenge name, `graveyard`.

## 6. Dead ends checked

- **Acrostics** — first letters of paragraphs (`DEIBIIeIST`) and of sentences
  within each paragraph produced nothing.
- **Capitalized proper nouns** (`Hallmark`, `Little Alex`, `Sunday`) — flavor,
  not a channel.
- **Whitespace / byte-level stego** — no trailing-whitespace encoding, no
  non-ASCII, no zero-width characters, nothing appended past EOF.

## 7. Takeaways

1. **Always validate a substitution key as a bijection.** A key that produces
   readable output can still be wrong; a collision or an unmapped plaintext
   letter is proof of an error, and it will sit exactly where the author hid the
   payload.
2. **Rare ciphertext letters are high-value.** A character appearing once in
   2 KB is almost certainly load-bearing — derive it from its own context, never
   by assuming the surrounding word is spelled normally.
3. **Don't autocorrect the plaintext.** Deliberate misspellings and odd
   capitalization inside a flag string are signal, not noise.
