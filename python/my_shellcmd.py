#!/usr/bin/python3
#
# Simple reusable class to execute shell commands.

import subprocess
import os
import smtplib

from subprocess import CalledProcessError

class ShellCmdClass:
	
	Name = "ShellCmdClass"

	def __init__(self, the_cmd):
		self.cmd = the_cmd
	
	def runcmd(self):
		return subprocess.call(self.cmd)
	def runcmd_subprocess(self):
		return subprocess.Popen(self.cmd, stdout=subprocess.PIPE)
	def runcmd_chkoutput(self):
		output=""
		try:
			return subprocess.check_output(self.cmd)
		except subprocess.CalledProcessError as exc:
			return exc.output
	def runcmd_getoutput(self):
		return subprocess.check_output(self.cmd)
	def runcmd_os(self):
		return os.popen("%s" % (self.cmd), 'r+')


