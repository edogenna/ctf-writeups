import sys
nums = list(map(int, open(sys.argv[1] if len(sys.argv) > 1 else "numerophobia.txt").read().split()))
# every other number (even indices) had 13 added; undo it
chars = [chr(n - 13 if i % 2 == 0 else n) for i, n in enumerate(nums)]
print("".join(chars)[::-1])  # dyslexia: read it backwards
