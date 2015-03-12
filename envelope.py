#!/usr/bin/python

# TODO: radio button to select envelope size
# TODO: allow entry of return address with default
# TODO: show/hide return address box
# TODO: remember addresses printed, allow user to select
# TODO: improve css for rounding corners, image gradient, etc.
# Done: 
# 20150303: Figured out CGI, form, call to shell: works
# 20140305: bring bash script into python, calling enscript directly
# 20150305: output result from enscript to printing screen

import cgi
import subprocess 
import socket # for hostname

DEBUG = 1 #disable printing while testing

# Required header that tells the browser how to render the HTML.
print "Content-Type: text/html\n\n"
print "<HTML>"
print "<HEAD>"
print "<link rel='stylesheet' type='text/css' href='buttons.css' media='screen' />"
print "<TITLE>Print an Envelope</TITLE>"
print "</HEAD>"
print "<BODY>"

def displayForm():
	print "<h3>Print an Envelope on ", socket.gethostname(), "</h3>\n"
	print "<FORM METHOD=post ACTION=\"envelope.py\">\n"

	# TODO seed fromaddress from server/browser history
	# TODO on-load, hide fromaddress when non-empty
	#print "<p>From:</p>\n"
	#print "<div><textarea name=\"fromaddress\" cols=40 rows=5></textarea></div>\n"
	
	print "<p>To:</p>\n"
	print "<div><textarea name=\"toAddress\" cols=40 rows=5></textarea></div>\n"

	print "<INPUT TYPE=hidden NAME =\"action\" VALUE=\"print\">\n"
	print "<INPUT TYPE=submit VALUE=\"Enter\">\n"
	print "</FORM>\n"


def displayResults(address, result):
	print "<h3>Printed address:</h3>"
	print "<pre style=\"background-color:#faf8f0; outline: 1px solid black; padding:5px;\">"
	print '\n'.join(address)
	print "</pre>"
	print "<p>OS responded: ", result, "</p>\n"
	print "<p></p>"
	print "<p><a href='./envelope.py' class='button large black'>Print another</a></p>"


def sanitizeAddress(toAddress):
	result = []
	for line in toAddress.splitlines():
		candidate = line.strip().replace('"','').replace('`','')
		if len(candidate) > 0:
			result.append(candidate)
	return result


def print_envelope(toAddress):

	returnAddress="-"
	returnAddressFile="/home/pi/Documents/tef/secrets/returnAddress.txt"
	try:
		with open(returnAddressFile) as f:
			returnAddress = f.read()
	except Exception:
		pass

	vmargin = "\n" * 6
	hmargin = " " * 20
	content = (returnAddress + vmargin + 
			hmargin + ("\n" + hmargin).join(toAddress))

	cmd = ["/usr/bin/enscript", "--no-header", "--landscape", 
		"--font=CourierBold@12"]
	cmd.append("--margins=160:0:0:425")
	if DEBUG:
		return cmd
	else:
		process = subprocess.Popen(cmd,
				stdin=subprocess.PIPE, 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE)
		return process.communicate(content)


# Define main function.
def main():
	form = cgi.FieldStorage()
	if (form.has_key("action") and form.has_key("toAddress")):
		if (form["action"].value == "print"):
			toAddress = sanitizeAddress(form["toAddress"].value)
			result = print_envelope(toAddress)
			displayResults(toAddress, result)
	else:
		 displayForm()
	print "</BODY>\n"
	print "</HTML>\n"

# Call main function.
main()
