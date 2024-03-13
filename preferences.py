
class Preferences:
    def __init__(self, resolution, video, path, list_file_name, session_type):
        self.mResolution = resolution
        self.mVideo = video
        self.mPath = path
        self.mListFileName = list_file_name
        self.mSessionType = session_type

    def get_resolution(self):
        return self.mResolution

    def get_video(self):
        return self.mVideo

    def get_path(self):
        return self.mPath

    def get_list_file_name(self):
        return self.mListFileName

    def get_session_type(self):
        return self.mSessionType
