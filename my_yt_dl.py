import re
import urllib
from pytube import YouTube
import os

class youtubeHelper:

    def __init__(self):
        return

    def getSongLink(self, song):
        
        song = song.replace(" ", "+")
        song = song.encode('ascii', 'replace')
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + str(song))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_url = "https://www.youtube.com/watch?v=" + video_ids[0]

        return video_url

    def downloadSong(self, link, path):

        #get the video
        yt = YouTube(link)
        audio = yt.streams.filter(only_audio=True).first()

        #download to folder
        file = audio.download(output_path=path)

        #save as mp3
        base, ext = os.path.splitext(file)
        new_file = base + '.mp3'
        os.rename(file, new_file)
