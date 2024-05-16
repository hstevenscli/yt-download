from pytube import YouTube
from pytube import Search
from preferences import Preferences
import yaml



def get_preferences():
    #read config.yaml
    DEFAULT_PREFERENCES = "default_preferences"
    USER_PREFERENCES = "user_preferences"
    PREFERENCES = [DEFAULT_PREFERENCES, USER_PREFERENCES]
    pptr = 1
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    if USER_PREFERENCES not in config:
        pptr = 0

    resolution = config[PREFERENCES[pptr]]["resolution"]
    video = config[PREFERENCES[pptr]]["video"]
    path = config[PREFERENCES[pptr]]["path"]
    list_file_name = config[PREFERENCES[pptr]]["list-file-name"]
    session = config[PREFERENCES[pptr]]["session"]
    p = Preferences(resolution, video, path, list_file_name, session)
    return p

# For displaying download progress on large downloads
def on_progress_callback(stream, chunk, bytes_remaining):
    """
    Callback function to track the download progress.
    """
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Downloaded: {percentage:.2f}%")

# parse a list of urls from a file
def get_list_of_urls(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
    f.close()
    return lines

# Choose resolution or audio only for when downloading a single video
def set_url_and_stream(preferences):
    url = input("URL: ")
    if url == "" or url is None:
        # url = "https://www.youtube.com/watch?v=i43tkaTXtwI"
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    yt = YouTube(url, on_progress_callback=on_progress_callback)


    if str(preferences.get_video()) == "video":
        res = preferences.get_resolution()
        stream = yt.streams.get_by_resolution(str(res))
        if stream is None:
            stream = yt.streams.get_highest_resolution()
        # if res == "720":
        #     stream = yt.streams.get_by_itag(22)
        #     if stream is None:
        #         stream = yt.streams.get_highest_resolution()
        # elif res == "max":
        #     stream = yt.streams.get_highest_resolution()
    else:
        stream = yt.streams.get_audio_only()
    return yt, stream

# Download all videos in a list of urls provided
def download_from_list(list_of_urls, preferences):
    for url in list_of_urls:
        yt = YouTube(url, on_progress_callback=on_progress_callback)
        stream = yt.streams.get_audio_only()
        name = stream.default_filename
        path = preferences.get_path()
        downloaded = stream.download(path, name)
        if downloaded:
            print()
            print(f"Video \"{name}\" downloaded to {path}")
            print(stream.filesize)
            print(yt.description)

# Works with yt_search or any yt object. Downloads a video with highest resolution given a yt object
def download_given_yt_object(ytobject, preferences):
    stream = ytobject.streams.get_highest_resolution()
    name = stream.default_filename
    path = preferences.get_path()
    downloaded = stream.download(path, name)
    if downloaded:
        print()
        print(f"Video \"{name}\" downloaded to {path}")
        print(stream.filesize)

# Search given a query and returns a list of results
def yt_search(query, preferences):
    s = Search(query)
    i = 0
    for video in s.results:
        print(str(i) + ":", video.title)
        i += 1
    user_choice = int(input("Which result would you like to download?\n> "))
    # print(s.results)
    print()
    print(s.completion_suggestions)
    print(len(s.results))
    download_given_yt_object(s.results[user_choice], preferences)

# Download a single video given a url, rename this to something other than main
def download_single_url(preferences):
    yt, stream = set_url_and_stream(preferences)
    name = stream.default_filename
    path = preferences.get_path()
    downloaded = stream.download(path, name)
    if downloaded:
        print()
        print(f"Video \"{name}\" downloaded to {path}")
        print(stream.filesize)
        print(yt.description)

def choose_method_of_download():
    preferences = get_preferences()
    choice = input("Single url or list of url? \n>url\n>list\n>search\n>")
    if choice == "url":
        download_single_url(preferences)
        return
    elif choice == "list":
        urls = get_list_of_urls("urls.txt")
        download_from_list(urls, preferences)
        return
    elif choice == "search" or choice in "search":
        query = input("Search for a video: ")
        yt_search(query, preferences)
    else:
        choose_method_of_download()

# yt_search("me myself and i geazy")
choose_method_of_download()
# p = get_preferences()
# print(p.mPath)
# print(p.mResolution)
# print(p.mVideo)
# print(p.mListFileName)
# print(p.mSessionType)
