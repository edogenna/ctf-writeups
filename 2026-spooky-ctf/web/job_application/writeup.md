# Dad Joke Generator — CTF Writeup

**Flag:** `spooky{th4t_w4snt_funn3h}`

## Challenge Overview

A web page at `http://18.217.64.238/` presents a "Dad Joke Generator" with a garish UI (animated rainbow background, spinning doge, Comic Sans everywhere). Clicking the button navigates to a random joke page. The URL paths are long strings of only uppercase and lowercase letters, hinting at some encoding scheme.

## Recon

Saving the page locally reveals two key files:

- `testindex2.js` — contains a `textData` array of 46 Base64-encoded strings, each used as a URL path
- `aa.html` — the main page; `generateJoke()` picks a random entry from `textData` and navigates to it

The comment at the top of the saved HTML file also leaks the URL path of the current page, e.g.:

```
<!-- saved from url=(0173)http://18.217.64.238/RUVFRUVFRUVFZWVFRWVF...== -->
```

## Cracking the Encoding

Decoding one of the `textData` entries from Base64 gives something like:

```
EEEEEeEEEEeEeEEEEeEEEEEEEEEEEEEeEEEEeEEEeEEeEE...
```

The result only contains `E` (uppercase) and `e` (lowercase) — a two-symbol alphabet, which immediately suggests binary encoding: **E = 0, e = 1**.

Interpreting the resulting bit string in 16-bit chunks (big endian) decodes cleanly to ASCII text:

```
EEEEEEEEEeEEEEEE  →  0000000001000000  →  U+0066  →  'p'
```

This is UTF-16 Big Endian (UTF-16BE): each character is a 2-byte code point, MSB first.

### Full 3-layer scheme

```
Encode:  text  ──►  UTF-16BE bytes  ──►  bits → E/e string  ──►  Base64  ──►  URL path
Decode:  URL path  ──►  Base64  ──►  E/e string  ──►  bits (E=0, e=1)  ──►  16-bit chunks  ──►  text
```

### Python decode function

```python
import base64

def decode_path(s):
    padded = s + '=' * (4 - len(s) % 4)
    raw = base64.b64decode(padded).decode('ascii')
    bits = ''.join('0' if c == 'E' else '1' for c in raw)
    text = ''
    for i in range(0, len(bits) - 15, 16):
        cp = int(bits[i:i+16], 2)
        if cp > 0:
            text += chr(cp)
    return text
```

Applying this to all 46 entries in `textData` yields joke category names like `pirate`, `dad-bod`, `knock-knock`, etc.

### Python encode function

```python
def encode_path(word):
    ee = ''
    for byte in word.encode('utf-16-be'):
        for bit in range(7, -1, -1):
            ee += 'e' if (byte >> bit) & 1 else 'E'
    return base64.b64encode(ee.encode('ascii')).decode('ascii')
```

## Finding the Flag

The `textData` array only lists joke category paths — nowhere is a `/flag` endpoint mentioned. However, since the encoding is fully reversible, any arbitrary path can be encoded and requested directly.

Encoding the word `flag` and requesting that path:

```python
encoded = encode_path('flag')
# → RUVFRUVFRUVFZWVlRUVFRUVFRUVFRUVFRWVl...
```

```
GET http://18.217.64.238/<encoded>
```

The server responds with a joke page whose `<h3>` contains the flag:

```
spooky{th4t_w4snt_funn3h}
```

## Bonus Observations

- **Three 403 pages:** Paths decoding to `construction`, `captain-hook`, and `french-fries` return HTTP 403. The pun: *Captain Hook is under construction.*
- **Incomplete entry:** Index 45 decodes to `apple-` with 14 leftover bits — the encoded word is truncated mid-character, suggesting the full path was `apple-pie` or similar.
- **Steganography dead end:** `doge.jpg` ends cleanly with no data appended after the JPEG end marker (`FFD9`); no hidden content.
