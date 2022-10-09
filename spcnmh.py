#!/usr/bin/env python3

# Note that running python with the `-u` flag is required on Windows,
# in order to ensure that stdin and stdout are opened in binary, rather
# than text, mode.

VERSION = "1.0.0"

import json
import sys
import struct

# Read a message from stdin and decode it.
def get_message():
	raw_length = sys.stdin.buffer.read(4)

	if not raw_length:
		sys.exit(0)
	message_length = struct.unpack('=I', raw_length)[0]
	message = sys.stdin.buffer.read(message_length).decode("utf-8")
	return json.loads(message)

# Send an encoded message to stdout.
def send_message(message):
	# Encode a message for transmission, given its content.
	def encode_message(message_content):
		encoded_content = json.dumps(message_content).encode("utf-8")
		encoded_length = struct.pack('=I', len(encoded_content))
		# use struct.pack("10s", bytes), to pack a string of the length of 10 characters
		return {'length': encoded_length, 'content': struct.pack(str(len(encoded_content))+"s",encoded_content)}
	encoded_message = encode_message(message)
	sys.stdout.buffer.write(encoded_message['length'])
	sys.stdout.buffer.write(encoded_message['content'])
	sys.stdout.buffer.flush()

message = get_message()
if path := message.get("path"):
	import subprocess
	if cwd := message.get("cwd"):
		import os
		cwd = os.path.expandvars(os.path.expanduser(cwd))
	subprocess.Popen(path, cwd = cwd, shell = True, creationflags = subprocess.CREATE_BREAKAWAY_FROM_JOB if sys.platform == "win32" else 0)
send_message({
	"version": VERSION,
	"message": message
})
