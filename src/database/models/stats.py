class Stats:
    def __init__(self, digg_count, play_count, share_count, comment_count):
        self.comment_count = comment_count
        self.digg_count = digg_count
        self.play_count = play_count
        self.share_count = share_count

    def to_dict(self):
        stats_dict = {
            "commentCount": self.comment_count,
            "diggCount": self.digg_count,
            "playCount": self.play_count,
            "shareCount": self.share_count,
        }
        return stats_dict