class VoiceChat:
    def __init__(self):
        self.rooms = {}
        self.room_count = 0

    def create_room(self):
        self.room_count += 1

        self.rooms[self.room_count] = {
            'room_id': self.room_count,
            'messages': []
        }

        return self.rooms[self.room_count]

    def create_voice_room(self):
        self.room_count += 1

        self.rooms[self.room_count] = {
            'room_id': self.room_count,
            'messages': []
        }

        return self.rooms[self.room_count]

    def get_room_count(self):
        return self.room_count

    def get_messages(self, room):
        return self.rooms[room]['messages']

    def add_message(self, room, user, content):
        message = {
            'user': user,
            'content': content
        }

        self.rooms[room]['messages'].append(message)

        return self.rooms[room]