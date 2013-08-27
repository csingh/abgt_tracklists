from bs4 import BeautifulSoup
import urllib.request
import sys

TRACKLIST_FILENAME = "tracklist.txt"

BASE_URL = "http://www.aboveandbeyond.nu/radio/abgt"
TITLE_SELECTOR = "div.title-super h1"
TRACKLIST_SELECTOR = "div.field-type-text-with-summary div div p"


for x in range(10):

	# make url
	abgt_num = x
	zeroes = "0" * (3 - len(str(abgt_num)))
	abgt_url_num =  zeroes + str(abgt_num)
	full_url = BASE_URL + abgt_url_num

	print("Getting tracklist for ABGT " + abgt_url_num)

	# parse
	try:
		with urllib.request.urlopen(full_url) as url:
			print("Opened URL: ", full_url)

			soup = BeautifulSoup(url.read())

			# title stuff
			title_tag = soup.select(TITLE_SELECTOR)[0]
			title_text = title_tag.get_text()

			# tracklist stuff
			tracklist_tag = soup.select(TRACKLIST_SELECTOR)[0]
			tracklist = tracklist_tag.get_text().split("\n")

			# write to file
			with open(TRACKLIST_FILENAME, "a") as f:
				f.write(title_text)
				f.write("\n")
				for track in tracklist:
					# TODO: kinda ugly, see if there is better way?
					f.write(track.encode("ascii", "ignore").decode("utf-8"))
					f.write("\n")
				f.write("\n------------------------------------------------------\n")

	except urllib.error.HTTPError:
		print("ERROR: Could not open URL '" + full_url + "'")
