---
tags: [_BOF, _printf, _shellcode, _stack_leak, TJCTF]
title: Osrs
created: '2020-05-31T17:35:28.671Z'
modified: '2020-05-31T19:12:06.466Z'
---

# Osrs
> My friend keeps talking about Old School RuneScape. He says he made a service to tell you about trees.
> I don't know what any of this means but this system sure looks old! It has like zero security features enabled...
## Solving
### General information
- 32 bit
- No security enabled
### Exploiting
In `get_tree`, there's a `gets` into a $256$ byte long buffer.
Using `pattern create 300` in `gdb`, running the binary and then `pattern search`, we find that the offset to `EIP` is $272$ bytes

When running `get_tree`, on a tree that doesn't exist, it prints the `%d` address of the buffer. It's the two complement of hex, and we can turn it into the correct version by adding $2^{32} or 1<<32$

So our first payload will be
- Overflow and get address
- Return to `get_tree`
Then our second payload will be
- Shellcode
- Overflow buffer
- Return to stack address

### Code
```bash
python -c "print(
  'a' * 272 + # Padding
  'bbbb' # Return address
);" > input.txt
```
