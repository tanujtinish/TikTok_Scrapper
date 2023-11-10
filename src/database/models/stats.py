class Stats:
    def __init__(self, digg_count, play_count, share_count, comment_count):
        self.comment_count = comment_count
        self.digg_count = digg_count
        self.play_count = play_count
        self.share_count = share_count

    def to_dict(self):
        stats_dict = {
            "commentCount": str(self.comment_count),
            "diggCount": str(self.digg_count),
            "playCount": str(self.play_count),
            "shareCount": str(self.share_count),
        }
        return stats_dict
    
    @staticmethod
    def from_dict(stats_dict):
        
        return Stats(
            int(stats_dict["diggCount"]),
            int(stats_dict["playCount"]),
            int(stats_dict["shareCount"]),
            int(stats_dict["commentCount"])
        )