# from pytube import Playlist 
# from pytube import YouTube

# link = input("Enter YouTube Playlist URL: ")

# yt_playlist = Playlist(link)

# for video in yt_playlist.videos:
#     video.streams.get_by_resolution("360p").download()
#     print("Video Downloaded: ", video.title)

# print("\nAll videos are downloaded.")
# from pytube import Playlist 
# from pytube import YouTube

# link = input("Enter YouTube Playlist URL: ")

# yt_playlist = Playlist(link)
import os
import time
from urllib.error import HTTPError, URLError
from http.client import IncompleteRead
from pytube import Playlist 
from pytube import YouTube

def sanitize_filename(filename):
    invalid_chars = ['/', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

link = input("Enter YouTube Playlist URL: ")
output_directory = "C:\\Users\\palla\\Desktop\\PROGRAMS\\Playlistdownloader\\Playlist"

yt_playlist = Playlist(link)

# Get the number of videos in the playlist
num_videos = len(yt_playlist.video_urls)

# Ask the user for the number of already downloaded lectures
already_downloaded = int(input("Enter the number of already downloaded lectures: "))

# Ensure that already_downloaded is not greater than the number of videos in the playlist
if already_downloaded > num_videos:
    print(f"Error: The playlist only contains {num_videos} videos.")
    already_downloaded = num_videos

# Create the directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Convert the videos generator to a list
videos = list(yt_playlist.videos)

for i, video in enumerate(videos[already_downloaded:], start=already_downloaded+1):
    sanitized_title = sanitize_filename(video.title)
    stream = video.streams.filter(file_extension='mp4').get_highest_resolution()
    if stream is not None:
        attempts = 0
        while attempts < 3:
            try:
                stream.download(output_path=output_directory, filename=f"Lecture {i} - {sanitized_title}.mp4")
                print(f"Video Downloaded: Lecture {i} - {sanitized_title}")
                print("Resolution: ", stream.resolution)
                break
            except (HTTPError, URLError) as e:
                attempts += 1
                print(f"HTTP error {e.code}, retrying... ({attempts} attempts)")
                if e.code == 503:
                    print("Service unavailable, retrying in 5 seconds...")
                    time.sleep(5)
            except IncompleteRead:
                attempts += 1
                print(f"IncompleteRead error, retrying... ({attempts} attempts)")
                time.sleep(5)
            if attempts == 3:
                print(f"Failed to download video after 3 attempts: Lecture {i} - {sanitized_title}")
    else:
        print("Stream with highest resolution not found for video: ", sanitized_title)

print("\nAll videos are downloaded.")