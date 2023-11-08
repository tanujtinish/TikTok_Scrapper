class Author:
    def __init__(self, author_data, author_stats_data):
        self.avatar_larger = author_data.get("avatarLarger", "")
        self.avatar_medium = author_data.get("avatarMedium", "")
        self.avatar_thumb = author_data.get("avatarThumb", "")
        self.comment_setting = author_data.get("commentSetting", 0)
        self.download_setting = author_data.get("downloadSetting", 0)
        self.duet_setting = author_data.get("duetSetting", 0)
        self.ftc = author_data.get("ftc", False)
        self.id = author_data.get("id", "")
        self.is_ad_virtual = author_data.get("isADVirtual", False)
        self.is_embed_banned = author_data.get("isEmbedBanned", False)
        self.nickname = author_data.get("nickname", "")
        self.open_favorite = author_data.get("openFavorite", False)
        self.private_account = author_data.get("privateAccount", False)
        self.relation = author_data.get("relation", 0)
        self.sec_uid = author_data.get("secUid", "")
        self.secret = author_data.get("secret", False)
        self.signature = author_data.get("signature", "")
        self.stitch_setting = author_data.get("stitchSetting", 0)
        self.tt_seller = author_data.get("ttSeller", False)
        self.unique_id = author_data.get("uniqueId", "")
        self.verified = author_data.get("verified", False)

        self.digg_count = author_stats_data.get("diggCount", 0)
        self.follower_count = author_stats_data.get("followerCount", 0)
        self.following_count = author_stats_data.get("followingCount", 0)
        self.friend_count = author_stats_data.get("friendCount", 0)
        self.heart = author_stats_data.get("heart", 0)
        self.heart_count = author_stats_data.get("heartCount", 0)
        self.video_count = author_stats_data.get("videoCount", 0)

    def to_dict(self):
        # Convert the Author object to a dictionary
        author_dict = {
            "avatar_larger": self.avatar_larger,
            "avatar_medium": self.avatar_medium,
            "avatar_thumb": self.avatar_thumb,
            "comment_setting": self.comment_setting,
            "download_setting": self.download_setting,
            "duet_setting": self.duet_setting,
            "ftc": self.ftc,
            "id": self.id,
            "is_ad_virtual": self.is_ad_virtual,
            "is_embed_banned": self.is_embed_banned,
            "nickname": self.nickname,
            "open_favorite": self.open_favorite,
            "private_account": self.private_account,
            "relation": self.relation,
            "sec_uid": self.sec_uid,
            "secret": self.secret,
            "signature": self.signature,
            "stitch_setting": self.stitch_setting,
            "tt_seller": self.tt_seller,
            "unique_id": self.unique_id,
            "verified": self.verified,
        }
        author_stats_dict = {
            "digg_count": self.digg_count,
            "follower_count": self.follower_count,
            "following_count": self.following_count,
            "friend_count": self.friend_count,
            "heart": self.heart,
            "heart_count": self.heart_count,
            "video_count": self.video_count,
        }
        return {"author_data": author_dict, "author_stats_data": author_stats_dict}