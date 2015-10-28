# This program will try to crack an md5 hash using the search
# results aquired from google.
#
# @author    Wadie Assal

import sys
import urllib2
import re
import hashlib
from xgoogle.search import GoogleSearch

# Try's to find a match from all the data
def findhash( md5hash ):
	# Set the header before reqeusting all the data
	# This is NOT for the google search
	headers = {'User-Agent' : 'Mozilla 5.10'}

	# Get all the urls with the posible password
	urls = search( md5hash )
	words = []

	for url in urls:
		try:
			request = urllib2.Request(url, None, headers)
			response = urllib2.urlopen(request)
			html = response.read()
			data = remove_extra_spaces(  remove_html_tags(html) )
			words = words + data.split()
		except Exception, e:
			print "ERROR: Could not retrieve URL"

	for word in words:
		if hashlib.md5( word ).hexdigest() == md5hash:
			print "Password of hash " + md5hash + " is " + word
			break


# Searches google with the specified md5 hash.
# 
# @ return
def search( md5hash ):
	urls = []

	gs = GoogleSearch( md5hash )
	gs.results_per_page = 100
	results = gs.get_results()

	for res in results:
		urls.append( res.url.encode('utf8')  )

	return urls


# Strip all the html tags
def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


# Remove extra spaces
def remove_extra_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)    


# Main function of this program
def main():

    # parse command line options
	for arg in sys.argv[1:]:
		findhash( arg )

# Checks if this file is started as a regular program
if __name__ == "__main__":
    main()
