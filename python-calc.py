#!/usr/bin/python3
import sys

a = int(sys.argv[1])
b = int(sys.argv[3])
operaciya = sys.argv[2]
if operaciya == "+":
	print(a + b)
else:
	exit 0
