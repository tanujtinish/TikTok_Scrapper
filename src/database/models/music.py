class Music:
    def __init__(self, title, author_name, album ):
        self.album = album
        self.author_name = author_name
        self.title = title
    
    def to_dict(self):
        # Convert the Music object to a dictionary
        music_dict = {
            "album": self.album,
            "author_name": self.author_name,
            "title": self.title,
        }
        return music_dict
    
    @staticmethod
    def from_dict(music_dict):
        
        title = music_dict.get("title", "")
        author_name = music_dict.get("author_name", "")
        album = music_dict.get("album", "")
        
        music= Music(
            title, author_name, album
        )
        return music