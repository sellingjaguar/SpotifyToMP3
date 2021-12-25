import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib
from bs4 import BeautifulSoup

class spotipyHelper:

    sp = None
    user_page = None
    username = None
    playlist_name = None
    
    def __init__(self, cId, sec):
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=cId, client_secret=sec))

    #set the user link page
    def setUserPage(self, user_page):
        self.user_page = user_page
        try:
            self.username = user_page.replace("https://open.spotify.com/user/", "")
            self.username = username[:username.index("?")]
        except:
            True

    #link to user display name
    def getUserDisplayName(self):
        html = urllib.request.urlopen(self.user_page).read()
        display_name = BeautifulSoup(html, "lxml").find("meta", property="og:title")
        display_name = display_name["content"]
        return display_name

    #loop trough playlist (bypassing the 50 limit)
    def getPlaylistList(self):
        sp = self.sp
        username = self.username
        c = 0
        repeat = True
        playlist_count = 0
        playlist_list = []
        
        while repeat:
            #list playlists
            playlists = sp.user_playlists(username, 50, 50 * c)
            for i, playlist in enumerate(playlists['items']):
                playlist_count += 1
                playlist_list.append("%d - %s" % (playlist_count, playlist['name']))

            #check if more playlists exist beyond the spotify limit
            exists = False
            playlists = sp.user_playlists(username, 50, 50 * (c+1))
            for i, playlist in enumerate(playlists['items']):
                exists = True
                break
            if exists:
                c+=1
            else:
                repeat = False

        return playlist_list

    def getSongList(self, choice):
        sp = self.sp
        username = self.username

        #calculate the offset
        c=0
        choice -= 1
        while choice - 50 >= 0:
            choice -= 50
            c += 1
        playlists = sp.user_playlists(username, 50, 50 * c)

        #get song names
        song_names = []
        for i, playlist in enumerate(playlists['items']):

            #if selected playlist
            if i == choice:

                self.playlist_name = playlist['name']
                
                #check for tracks over the spotify api limit
                track_count = playlist['tracks']['total']
                c = 0
                while track_count - 100 >= 0:
                    track_count -= 100
                    c += 1

                #loop trough tracks
                for i in range(0, c+1):
                    tracks = sp.playlist_tracks(playlist['id'], None, 100, 100 * i)
                    bad = 0
                
                    for j, item in enumerate(tracks['items']):
                        track = item['track']

                        #check if track is valid
                        if not track['name'] == "":
                    
                            name = "%s - %s" % (track['name'], track['artists'][0]['name'])
                            #song_names.append("%d - %s" % (j + 1 - bad + (100*i) ,name))
                            song_names.append(name)
                            #name = name.replace(" ", "+")
                    
                            #songs.append(name)
                        else:
                             bad += 1

                break

        return song_names

    def getPlaylistName(self):
        return self.playlist_name
        
        
