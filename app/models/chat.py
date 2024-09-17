import json
from datetime import datetime

class Chat():
    def __init__(self) -> None:
        self.filepath = 'chat.json'
        self.room_count = self.get_room_count()

    def get_room_count(self):
        with open(self.filepath, 'r') as file:
            data = json.load(file)
            room_count = data.get('room_count')

            return room_count
        
    def add_message(self, room : int, user : str, content : str):
        with open(self.filepath, 'r+') as file:
            data = json.load(file)

            room_data = data.get(f'{room}')

            if room_data is None:
                raise ValueError(f"Room {room} does not exist")

            messages = room_data.get('messages')

            messages.append(
                {
                    "user" : user,
                    "content" : content ,
                    "datetime" : datetime.now().isoformat()
                }
            )

            data[f'{room}']['messages'] = messages

            file.seek(0)

            json.dump(data, file, indent=2)

            file.truncate()

        return self.get_messages(room=room)

    def get_messages(self, room : int) -> list:

        with open(self.filepath, 'r') as file:
            data = json.load(file)

            room_data = data.get(f'{room}')

            if room_data is None:
                raise ValueError(f"Room {room} does not exist")

            room_messages : list = room_data.get('messages')

            return room_messages.copy()
        
    def create_room(self):
        with open(self.filepath, 'r+') as file:
            data = json.load(file)

            new_room_id = int(data.get('room_count', 0)) + 1

            # Create a new room entry
            data[str(new_room_id)] = {
                "room_id": new_room_id,
                "messages": [
                    {
                        "user": "SYSTEM",
                        "content": "Room created", 
                        "datetime": datetime.now().isoformat()
                    }
                ]
            }

            data['room_count'] = new_room_id

            self.room_count = new_room_id

            file.seek(0)
            
            json.dump(data, file, indent=2)
            
            file.truncate()

        return self.get_messages(room=new_room_id)