import sys

def notify(msg):
	sys.stdout.write("\r{:<80}".format(str(msg)))
	sys.stdout.flush()
