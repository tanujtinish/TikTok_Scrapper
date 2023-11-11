class Author:
    def __init__(self, id, nickname, unique_id, verified):

        self.id = id
        self.nickname = nickname
        self.unique_id = unique_id
        self.verified = verified

    def to_dict(self):
        author_dict = {
            "id": self.id,
            "nickname": self.nickname,
            "unique_id": self.unique_id,
            "verified": str(self.verified),
        }
        return author_dict
    
    @staticmethod
    def from_dict(author_dict):
        
        if type(author_dict.get("verified", False))==bool:
            verified = author_dict.get("verified", False)
        else:
            verified = True if author_dict.get("verified", False).lower() == "true" else False
            
        author= Author(
            author_dict.get("id", ""),
            author_dict.get("nickname", ""),
            author_dict.get("unique_id", ""),
            verified
        )
        return author