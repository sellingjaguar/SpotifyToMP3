import my_spotify
import my_yt_dl
import os

#auth stuff
data = []
with open("secrets.txt") as f:
    data = f.readlines()

#set key values
cId = data[0]
sec = data[1]

#create class acess
sHelper = my_spotify.spotipyHelper(cId, sec)
ytHelper = my_yt_dl.youtubeHelper()

#fancy stuff
os.system("color A")
print('''
   _____             _   _  __         _          __  __ _____ ____   
  / ____|           | | (_)/ _|       | |        |  \/  |  __ \___ \  
 | (___  _ __   ___ | |_ _| |_ _   _  | |_ ___   | \  / | |__) |__) | 
  \___ \| '_ \ / _ \| __| |  _| | | | | __/ _ \  | |\/| |  ___/|__ <  
  ____) | |_) | (_) | |_| | | | |_| | | || (_) | | |  | | |    ___) | 
 |_____/| .__/ \___/ \__|_|_|  \__, |  \__\___/  |_|  |_|_|   |____/  
        | |                     __/ |                                 
        |_|                    |___/          github.com/sellingjaguar
''')

#get user id and display name
#user_page = input("User profile link (should look like 'https://open.spotify.com/user/something'):\n-->")
user_page = "https://open.spotify.com/user/gmq0utoa3xontktj7uf5cefw6"

sHelper.setUserPage(user_page)

print("\nUser %s's public playlists:\n" % (sHelper.getUserDisplayName()))

#get playlist list
playlist_list = sHelper.getPlaylistList()
for playlist in playlist_list:
    print(playlist)

#get chosen playlist
choice = int(input("\nWhich playlist do you want to download (1-%d)\n-->" % (len(playlist_list))))

#get tracks
song_list = sHelper.getSongList(choice)
print()
for i, song in enumerate(song_list):
    print("%d - %s" % (i+1, song))

#yt download
choice = int(input("\nWant to download this playlist? (yes - 1, no - 0)\n-->"))

if choice != 1:
    quit()


#get yt links
print("\nGenerating youtube links...")

links = []

for song in song_list:
    links.append(ytHelper.getSongLink(song))

for i in links:
    print(i)

#create folder for playlist
folder_name = sHelper.getPlaylistName()
folder_name = folder_name.replace(" ", "")
newpath = os.path.join(os.getcwd(), folder_name)
if not os.path.exists(newpath):
    os.makedirs(newpath)

#try to download
for i, link in enumerate(links):
    
    print("\nDownloading... %s" % (song_list[i]))

    ytHelper.downloadSong(link, folder_name)    
    
#finish
input("\nFinished... press Enter to close")

