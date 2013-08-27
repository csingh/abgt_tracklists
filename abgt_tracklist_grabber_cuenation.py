from bs4 import BeautifulSoup
import urllib.request
import re

# takes list of bs4.element.Tag's and returns
# dict mapping episode num -> <a> tag links
def get_links_dict(link_tags):
	links = {}

	for tag in link_tags:
		link_title = tag.get_text().strip()
		# if link tag has title
		if link_title:
			# look for Group Therapy xxx
			match = re.search('group therapy (\d+)', link_title,flags=re.IGNORECASE)

			# if title matches search
			if (match):
				episode_num = int(match.group(1))

				# only if links doesnt already have episode
				if (episode_num not in links):
					# add to dict	
					links[episode_num] = tag

	return links

# given the soup for an episode-page
# returns the title of episode
def get_title(soup):
	title_tag = soup.select("h2.title")[0]
	title = title_tag.get_text().strip() 

	# remove [] from end of title
	title_m = re.search('(.*?)\[.*?\]', title)
	if title_m:
		title = title_m.group(1)

	return title

# given the soup for an episode-page
# returns a list of strings corresp. to tracks
def get_tracks(soup):
	tracks = []
	rows = soup.select("table.tracklist tr")

	for row in rows:
		s = ""
		for child in row.children:
			classes = child['class']
			text = child.get_text()
			if ("timeindex" in classes):
				s += text
			elif ("trackindex" in classes):
				s += " " + text
			elif ("performertitle" in classes):
				s += " " + text
			elif ("length" in classes):
				s += " " + text

		# TODO: ugly, see if better way
		tracks.append(s.encode("ascii", "ignore").decode("utf-8"))

	return tracks

#--------------------------------------------------------------------------------------

BASE_URL = "http://cuenation.com/"
LIST_URL = "http://cuenation.com/?page=cues&folder=abgt"

# parse
try:
	with urllib.request.urlopen(LIST_URL) as list_page:
		print("Opened URL: ", LIST_URL)

		links_soup = BeautifulSoup(list_page.read())
		link_tags = links_soup.select(".list a")
		links = get_links_dict(link_tags)
		print(links.keys())

		episode_num = 2
		print("Episode:", episode_num)
		tag = links[episode_num]
		print("Tag:", tag)

		episode_url = BASE_URL + tag["href"]
		with urllib.request.urlopen(episode_url) as episode_page:
			print("Opened episode page: ", episode_url)

			episode_soup = BeautifulSoup(episode_page.read())

			print(get_title(episode_soup))
			for track in get_tracks(episode_soup):
				print(track)

except urllib.error.HTTPError:
	print("ERROR: Could not open URL '" + full_url + "'")
