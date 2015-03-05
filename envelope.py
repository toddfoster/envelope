#!/usr/bin/python

# 20140303: Figured out CGI, form, call to shell: works
# TODO: bring bash script into python, calling enscript directly
# TODO: output result from enscript to printing screen
# TODO: radio button to select envelope size
# TODO: allow entry of return address with default
# TODO: show/hide return address box
# TODO: remember addresses printed, allow user to select

# Import the CGI module
import cgi
import os

# Required header that tells the browser how to render the HTML.
print "Content-Type: text/html\n\n"

def generate_form():
	print "<HTML>\n"
	print "<HEAD><TITLE>Print an Envelope</TITLE></HEAD>\n"
	print "<h3>Print an Envelope</h3>\n"
	print "<FORM METHOD=post ACTION=\"envelope.py\">\n"

	# TODO seed fromaddress from server/browser history
	# TODO on-load, hide fromaddress when non-empty
	#print "<p>From:</p>\n"
	#print "<div><textarea name=\"fromaddress\" cols=40 rows=5></textarea></div>\n"
	
	print "<p>To:</p>\n"
	print "<div><textarea name=\"toaddress\" cols=40 rows=5></textarea></div>\n"

	print "<INPUT TYPE=hidden NAME =\"action\" VALUE=\"display\">\n"
	print "<INPUT TYPE=submit VALUE=\"Enter\">\n"
	print "</FORM>\n"
	print "</BODY>\n"
	print "</HTML>\n"


def generateResults(toaddress):
	print "<HTML>\n"
	print "<HEAD><TITLE>Envelope Printing</TITLE></HEAD>\n"
	print "<BODY>\n"
	print "<p>Printed address = </p>"
	print "<ul>\n"
	param = ""
	for line in toaddress.splitlines():
		line = line.strip()
		if len(line) > 0:
			line = line.replace('"','')
			line = line.replace('`','')
			param = param + "\"" + line + "\" "
			print "<li>", line, "</li>\n"
	print "</ul>\n"

	print "<p></p><p><a href=\"./envelope.py\"> Print another</a></p>"
	print "</BODY>\n"
	print "</HTML>\n"


def sanitizeAddress(toaddress):
	result = ""
	for line in toaddress.splitlines():
		line = line.strip()
		line = line.replace('"','')
		line = line.replace('`','')
		if len(line) > 0:
			result = result + line + "\n"
	return result


def parametizeAddress(toaddress):
	result = ""
	for line in toaddress.splitlines():
		result = result + "\"" + line + "\" "
	return result


def print_envelope(toaddress):
	toaddress = sanitizeAddress(toaddress)
	param = parametizeAddress(toaddress)
	cmd = "/home/pi/bin/envstationery " + param
	os.system(cmd)
	generateResults(toaddress)


# Define main function.
def main():
	form = cgi.FieldStorage()
	if (form.has_key("action") and form.has_key("toaddress")):
		if (form["action"].value == "display"):
			print_envelope(form["toaddress"].value)
	else:
		 generate_form()

# Call main function.
main()
