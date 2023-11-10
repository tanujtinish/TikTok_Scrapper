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
        
        author= Author(
            author_dict["id"],
            author_dict["nickname"],
            author_dict["unique_id"],
            True if author_dict["verified"].lower() == "true" else False
        )
        return author