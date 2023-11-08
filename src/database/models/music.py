class Music:
    def __init__(self, music_data):
        self.album = music_data.get("album", "")
        self.author_name = music_data.get("authorName", "")
        self.cover_large = music_data.get("coverLarge", "")
        self.cover_medium = music_data.get("coverMedium", "")
        self.cover_thumb = music_data.get("coverThumb", "")
        self.duration = music_data.get("duration", 0)
        self.id = music_data.get("id", "")
        self.original = music_data.get("original", False)
        self.play_url = music_data.get("playUrl", "")
        self.title = music_data.get("title", "")
    
    def to_dict(self):
        # Convert the Music object to a dictionary
        music_dict = {
            "album": self.album,
            "author_name": self.author_name,
            "cover_large": self.cover_large,
            "cover_medium": self.cover_medium,
            "cover_thumb": self.cover_thumb,
            "duration": self.duration,
            "id": self.id,
            "original": self.original,
            "play_url": self.play_url,
            "title": self.title,
        }
        return music_dict