from pytube import YouTube

def on_progress_callback(stream, chunk, bytes_remaining):
    """
    Callback function to track the download progress.
    """
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Downloaded: {percentage:.2f}%")

def get_list_of_urls(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
    f.close()
    return lines

def set_url_and_stream():
    url = input("URL: ")
    if url == "" or url is None:
        # url = "https://www.youtube.com/watch?v=i43tkaTXtwI"
        url = "https://www.youtube.com/watch?v=mIYUih6Vy78"

    yt = YouTube(url, on_progress_callback=on_progress_callback)

    res = input("Resolution? 720, max: ")
    if res == "720":
        stream = yt.streams.get_by_itag(22)
        if stream is None:
            stream = yt.streams.get_highest_resolution()
    elif res == "max":
        stream = yt.streams.get_highest_resolution()
    else:
        stream = yt.streams.get_audio_only()
    return yt, stream

def download_from_list(list_of_urls):
    for url in list_of_urls:
        yt = YouTube(url, on_progress_callback=on_progress_callback)
        stream = yt.streams.get_audio_only()
        name = stream.default_filename
        path = "/mnt/c/Users/Hunter/Videos/YouTube/"
        downloaded = stream.download(path, name)
        if downloaded:
            print()
            print(f"Video \"{name}\" downloaded to {path}")
            print(stream.filesize)
            print(yt.description)
# download audio from list
# get list of urls from file
# for url make yt object
# make stream with get audio only
# make name path and download

def main():
    yt, stream = set_url_and_stream()
    name = stream.default_filename
    path = "/mnt/c/Users/Hunter/Videos/YouTube/"
    downloaded = stream.download(path, name)
    if downloaded:
        print()
        print(f"Video \"{name}\" downloaded to {path}")
        print(stream.filesize)
        print(yt.description)

def choose_method_of_download():
    choice = input("Single url or list of url? \n>url\n>list\n>")
    if choice == "url":
        main()
        return
    elif choice == "list":
        urls = get_list_of_urls("urls.txt")
        download_from_list(urls)
        return
    else:
        choose_method_of_download()

choose_method_of_download()
# # Replace 'your_video_url' with the URL of the YouTube video you want to download.
# url = 'https://www.youtube.com/watch?v=i43tkaTXtwI'

# # Create a YouTube object
# yt = YouTube(url, on_progress_callback=on_progress_callback)

# # Get the highest resolution stream
# video_stream = yt.streams.get_highest_resolution()

# # Specify the destination where you want to save the video

# # Download the video
# video_stream.download(path)

# print("Download complete.")
