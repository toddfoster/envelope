#!/usr/bin/python

# Print envelopes; intended to run on my home server without external access.
# A learning experiment for python & cgi
# Todd Foster, March 2015
#
# TODO: remember addresses printed, associated return, allow user to select
#

import cgi
import subprocess 
import socket

DEBUG = 0 #disable printing while testing
if DEBUG:
	import cgitb; cgitb.enable()

returnAddressFile="/home/pi/Documents/tef/secrets/returnAddress.txt"

printSettings = {
	'small'     :{ 'newlines':4, 'spaces':30, 'margins':'180:0:0:330' },
	'large'     :{ 'newlines':7, 'spaces':40, 'margins':'160:0:0:120' },
	'stationery':{ 'newlines':6, 'spaces':20, 'margins':'155:0:0:425' }
	}

def displayForm():
	print "<h1>Print an Envelope on ", socket.gethostname(), "</h1>"
	print "<FORM METHOD=post ACTION='envelope.py'>"

	# TODO seed fromaddress from server/browser history
	fromAddress = ''
	try:
		with open(returnAddressFile) as f:
			fromAddress = sanitizeAddress(f.read())
	except Exception:
		pass

	toAddress = ''

	#----- Return Address ------
	print '''
		<div id='fromHidden' onclick='showhide()'>
		<h3>&#x25B6;From:</h3>
		</div>
		<div id='fromShowing' class='hidden' onclick='showhide()'>
		<h3>&#x25BC;From:</h3>
		</div>
		<div id='fromEntry' class='hidden'>
		<textarea name='fromAddress' class='yellowbackground' cols=40 rows=5>'''
	print '\n'.join(fromAddress)
	print '''</textarea>
		</div>
		'''
	
	#----- To Address ------
	print '''
		<h3>To:</h3>
		<div><textarea name='toAddress' class='yellowbackground' cols=40 rows=5> '''
	print '\n'.join(toAddress)
	print '''</textarea>
		</div>
		'''

	#----- Settings  / Enter -----
	print '''
		<p class='clear'>&nbsp;</p>
		<div class='clear'>
		'''

	#----- Envelope size selection------
	print '''
		<div id='sizeSelection' class='floatLeft bordered greybackground'>
		<h3>Envelope Size</h3>
		<input type='radio' name='size' value='stationery' checked>Stationery<br>
		<input type='radio' name='size' value='large'>Large #10<br>
		<input type='radio' name='size' value='small'>Small<br>
		<p></p>
		</div>
		'''

	#----- Enter Button ------
	print '''
		<div id='formSubmit' class='floatLeft'>
		<p></p>
		<INPUT TYPE=hidden NAME ='action' VALUE='print'>
		<INPUT TYPE=submit VALUE='Enter' class='button large green'>
		</FORM>
		</div>

		</div>
		'''


def displayResults(result):
	print "<p class='bold'>Printed address:</p>"
	print "<pre style='background-color:lightyellow; outline: 1px solid black; padding:5px;'>"
	print result[0]
	print "</pre>"
	print "<p>OS responded: ", result if DEBUG else result[1], "</p>\n"
	print "<p></p>"
	print "<p><a href='./envelope.py' class='button large green'>Print another</a></p>"


def sanitizeAddress(address):
	result = []
	for line in address.splitlines():
		candidate = line.strip().replace('"','').replace('`','')
		if len(candidate) > 0:
			result.append(candidate)
	return result


def print_envelope(fromAddress, toAddress, size):
	vmargin = "\n" * printSettings[size]['newlines']
	hmargin = " " * printSettings[size]['spaces']
	content = ('\n'.join(fromAddress) + vmargin + 
			hmargin + ("\n" + hmargin).join(toAddress))

	cmd = ["/usr/bin/enscript", "--no-header", "--landscape", 
		"--font=CourierBold@12"]
	cmd.append("--margins=" + printSettings[size]['margins'])
	if DEBUG:
		return [content, ' '.join(cmd)]
	else:
		process = subprocess.Popen(cmd,
				stdin=subprocess.PIPE, 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE)
		return [content, process.communicate(content)]


# Define main function.
def main():
	print '''
<meta http-equiv='content-type' content='text/html; charset=UTF-8'>
<HTML>
<HEAD>
<link rel='stylesheet' type='text/css' href='envelope.css' media='screen' />
<TITLE>Print an Envelope</TITLE>
<script src='show.js'></script>
</HEAD>
<BODY>
	'''
	form = cgi.FieldStorage()
	if (form.has_key("action") and 
	form.has_key("size")):
		if (form["action"].value == "print"):
			fromAddress = sanitizeAddress(form["fromAddress"].value) if form.has_key("fromAddress") else ''
			toAddress = toAddress = sanitizeAddress(form["toAddress"].value) if form.has_key("toAddress") else ''
			size = form["size"].value
			result = print_envelope(fromAddress, toAddress, size)
			displayResults(result)
	else:
		 displayForm()
	print '''
</BODY>
</HTML>
	'''

# Call main function.
main()
