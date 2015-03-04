#!/usr/bin/python

# Import the CGI module
import cgi

# Required header that tells the browser how to render the HTML.
print "Content-Type: text/html\n\n"

# Define function to generate HTML form.
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

# Define function display data.
def print_envelope(toaddress):
	print "<HTML>\n"
	print "<HEAD><TITLE>Envelope Printing</TITLE></HEAD>\n"
	print "<BODY>\n"
	print "Printed address = ", toaddress
	print "<ul>\n"
	for line in toaddress.splitlines():
		print "<li>", line, "</li>\n"
	print "</ul>\n"
	print "<p></p><p><a href=\"./envelope.py\"> Print another</a></p>"
	print "</BODY>\n"
	print "</HTML>\n"

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
