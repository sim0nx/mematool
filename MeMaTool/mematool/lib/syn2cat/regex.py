''' This file includes a bunch of commonly used regular expressions '''


email = r'\b[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+[A-Z]{2,4}\b'
date = r'^(19\d\d|2\d\d\d)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$'
phone = r'^\+(\d){1,3}\.(\d){4,}$' # +123.1234   after the dot, minimum 4 numbers
homeDirectory = r'^/home/[a-z0-9]*$'
loginShell = r'^/bin/[a-z0-9]*$'
