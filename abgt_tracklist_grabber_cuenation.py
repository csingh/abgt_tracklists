from bs4 import BeautifulSoup
import urllib.request
import sys

TRACKLIST_FILENAME = "tracklist.txt"
LIST_URL = "http://cuenation.com/?page=cues&folder=abgt"
LINKS_SELECTOR = ".list a"

# parse
try:
	with urllib.request.urlopen(LIST_URL) as url:
		print("Opened URL: ", LIST_URL)

		soup = BeautifulSoup(url.read())

		links = soup.select(LINKS_SELECTOR)

		for link in links:
			print(link)

except urllib.error.HTTPError:
	print("ERROR: Could not open URL '" + full_url + "'")
