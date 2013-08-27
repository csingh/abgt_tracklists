from bs4 import BeautifulSoup
import urllib.request
import sys

BASE_URL = "http://www.aboveandbeyond.nu/radio/abgt"
TITLE_SELECTOR = "div.title-super h1"
TRACKLIST_SELECTOR = "div.field-type-text-with-summary"

for x in [1]:
	abgt_num = x
	zeroes = "0" * (3 - len(str(abgt_num)))
	abgt_url_num =  zeroes + str(abgt_num)
	full_url = BASE_URL + abgt_url_num

	print("URL:", full_url)

	try:
		with urllib.request.urlopen(full_url) as url:
			soup = BeautifulSoup(url.read())

			#print(soup.prettify().encode("utf-8"))

			title = soup.select(TITLE_SELECTOR)[0]

			print(title.get_text())
	except urllib.error.HTTPError:
		print("Could not open URL: ", full_url)
	except:
		print("Unexpected error: ", sys.exc_info()[0])
