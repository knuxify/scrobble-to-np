#!/usr/bin/env python3
import urllib.request, json, sys

# Load settings
settings = json.loads(open('settings.json', 'r').read())

# Import any extra modules that we need
if settings.get('mastodon_enable') == 'true':
	from mastodon import Mastodon
if settings.get('run_once') == 'false':
	import time

# Set up Mastodon posting
if settings.get('mastodon_enable') == 'true':
	try:
		mastodon = Mastodon(
			client_id = settings.get('mastodon_client_key'),
			client_secret = settings.get('mastodon_client_secret'),
			access_token = settings.get('mastodon_access_token'),
			api_base_url = settings.get('mastodon_api_domain')
		)
	except:
		print('Something went wrong while connecting to the Mastodon API. Check if the mastodon settings are set correctly.')
		sys.exit()

# Posting function
def post(content):
	if settings.get('mastodon_enable') == 'true':
		try:
			mastodon.status_post(content, visibility=settings.get('mastodon_post_visibility'))
		except:
			print('Something went wrong while posting to Mastodon. Check if the mastodon settings are set correctly.')

# Define previous artist and name variables, since we check for them
# before we define them for the first time
previous_artist = str()
previous_song_name = str()

while True:
	# Get the data from the API.
	try:
		scrobble_api_json = urllib.request.urlopen("https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&format=json&limit=%s" % (settings.get('lastfm_username'), settings.get('lastfm_api_key'), settings.get('lastfm_loopcount')))
		data = json.loads(scrobble_api_json.read().decode())
		# These two variables are used to store all the artists and song names in the query,
		# so that they can be compared later on. We set them here to:
		#  - define them for the first time...
		#  - ...and clear them once the loop begins again.
		artists_in_query = list()
		song_names_in_query = list()
		# Looping over every track found in the query:
		for track in data['recenttracks']['track']:
			print("Track:")
			for key, value in track.items():
				if key == '@attr' and value['nowplaying'] == 'true':
					print("UPSTREAM WORKAROUND: last.fm's API adds the track they deem 'now playing' to the API request. Ignoring.")
					break
				elif key == 'artist':
					print('  - Artist: ' + value['#text'])
					artists_in_query.append(value['#text'])
					artist = str(value['#text'])
				elif key == 'name':
					print('  - Track name: ' + value)
					song_names_in_query.append(value)
					song_name = str(value)
				elif key == 'url':
					print('  - Link: ' + value)
					url = str(value)
	except:
		print("Something went wrong during the API fetch. Check if the lastfm settings are set correctly.")
	finally:
		# If all the artists and song names in the query match, and they're not the same
		# as the previous ones, set the new previous artist/song name and post the actual #np post.
		if len(set(artists_in_query)) <= 1 and len(set(song_names_in_query)) <= 1 and artist != previous_artist and song_name != previous_song_name:
			previous_artist = artist
			previous_song_name = song_name
			post("#np: %s - %s\n%s" % (artist, song_name, url))
	if settings.get('run_once') == 'true':
		sys.exit()
	else:
		print('\nLoop finished. Sleeping...')
		time.sleep(int(settings.get('run_interval')))
