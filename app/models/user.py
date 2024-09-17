
class User():
    def __init__(self, id, username) -> None:
        self.id = id
        self.username = username

    def get_username(self):
        return self.username
    
    def set_username(self, username:str):
        self.username = username