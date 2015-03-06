#!/usr/bin/python

# TODO: radio button to select envelope size
# TODO: allow entry of return address with default
# TODO: show/hide return address box
# TODO: remember addresses printed, allow user to select
# Done: 
# 20150303: Figured out CGI, form, call to shell: works
# 20140305: bring bash script into python, calling enscript directly
# 20150305: output result from enscript to printing screen

# Import the CGI module
import cgi
import subprocess

# Required header that tells the browser how to render the HTML.
print "Content-Type: text/html\n\n"

def generateForm():
	print "<HTML>\n"
	print "<HEAD><TITLE>Print an Envelope</TITLE></HEAD>\n"
	print "<h3>Print an Envelope</h3>\n"
	print "<FORM METHOD=post ACTION=\"envelope.py\">\n"

	# TODO seed fromaddress from server/browser history
	# TODO on-load, hide fromaddress when non-empty
	#print "<p>From:</p>\n"
	#print "<div><textarea name=\"fromaddress\" cols=40 rows=5></textarea></div>\n"
	
	print "<p>To:</p>\n"
	print "<div><textarea name=\"toAddress\" cols=40 rows=5></textarea></div>\n"

	print "<INPUT TYPE=hidden NAME =\"action\" VALUE=\"display\">\n"
	print "<INPUT TYPE=submit VALUE=\"Enter\">\n"
	print "</FORM>\n"
	print "</BODY>\n"
	print "</HTML>\n"


def generateResults(toAddress, result):
	print "<HTML>\n"
	print "<HEAD><TITLE>Envelope Printing</TITLE></HEAD>\n"
	print "<BODY>\n"
	print "<p>Printed address:</p>"
	print "<ul>\n"
	for line in toAddress:
		print "<li>", line, "</li>\n"
	print "</ul>\n"

	print "<p>OS responded: ", result, "</p>\n"

	print "<p></p><p><a href=\"./envelope.py\"> Print another</a></p>"
	print "</BODY>\n"
	print "</HTML>\n"


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
	process = subprocess.Popen(cmd,
			stdin=subprocess.PIPE, 
			stdout=subprocess.PIPE, 
			stderr=subprocess.PIPE)
	return process.communicate(content)
#, shell=False, 


# Define main function.
def main():
	form = cgi.FieldStorage()
	if (form.has_key("action") and form.has_key("toAddress")):
		if (form["action"].value == "display"):
			toAddress = sanitizeAddress(form["toAddress"].value)
			result = print_envelope(toAddress)
			generateResults(toAddress, result)
	else:
		 generateForm()

# Call main function.
main()
