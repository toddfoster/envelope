#!/usr/bin/python

# TODO: radio button to select envelope size
# TODO: show/hide return address box
# TODO: remember addresses printed, allow user to select
# Done: 
# 20150303: Figured out CGI, form, call to shell: works
# 20140305: bring bash script into python, calling enscript directly
# 20150305: output result from enscript to printing screen
# 20150312: allow entry of return address with default
# 20150313: improve css for rounding corners, image gradient, etc.

import cgi
import subprocess 
import socket # for hostname

DEBUG = 1 #disable printing while testing
if DEBUG:
	import cgitb; cgitb.enable()

returnAddressFile="/home/pi/Documents/tef/secrets/returnAddress.txt"

print "<meta http-equiv='content-type' content='text/html; charset=UTF-8'>"
print "<HTML>"
print "<HEAD>"
print "<link rel='stylesheet' type='text/css' href='buttons.css' media='screen' />"
print "<TITLE>Print an Envelope</TITLE>"
print "<script src='show.js'></script>"
print "</HEAD>"
print "<BODY>"

def displayForm():
	print "<h3>Print an Envelope on ", socket.gethostname(), "</h3>\n"
	print "<FORM METHOD=post ACTION='envelope.py'>"

	# TODO seed fromaddress from server/browser history
	print "<div id='fromHidden' onclick='showhide()'>"
	print "<p>&#x25B6;From:</p>"
	print "</div>"
	print "<div id='fromShowing' class='hidden' onclick='showhide()'>"
	print "<p>&#x25BC;From:</p>"
	print "</div>"
	print "<div id='fromEntry' class='hidden'>"
	print "<textarea name='fromAddress' cols=40 rows=5></textarea>"
	print "</div>"
	
	print "<p>To:</p>"
	print "<div><textarea name='toAddress' cols=40 rows=5></textarea></div>"

	print "<p></p>"

	print "<INPUT TYPE=hidden NAME ='action' VALUE='print'>"
	print "<INPUT TYPE=submit VALUE='Enter'>"
	print "</FORM>"


def displayResults(result):
	print "<h3>Printed address:</h3>"
	print "<pre style=\"background-color:#faf8f0; outline: 1px solid black; padding:5px;\">"
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


def print_envelope(fromAddress, toAddress):
	vmargin = "\n" * 6
	hmargin = " " * 20
	content = ('\n'.join(fromAddress) + vmargin + 
			hmargin + ("\n" + hmargin).join(toAddress))

	cmd = ["/usr/bin/enscript", "--no-header", "--landscape", 
		"--font=CourierBold@12"]
	cmd.append("--margins=160:0:0:425")
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
	form = cgi.FieldStorage()
	if (form.has_key("action") and 
	form.has_key("toAddress")):
		if (form["action"].value == "print"):
			fromAddress = ''
			if form.has_key("fromAddress"):
				fromAddress = sanitizeAddress(form["fromAddress"].value)
			if len(fromAddress) == 0:
				try:
					with open(returnAddressFile) as f:
						fromAddress = sanitizeAddress(f.read())
				except Exception:
					pass
			toAddress = sanitizeAddress(form["toAddress"].value)
			result = print_envelope(fromAddress, toAddress)
			displayResults(result)
	else:
		 displayForm()
	print "</BODY>\n"
	print "</HTML>\n"

# Call main function.
main()
