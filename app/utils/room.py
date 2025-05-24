from datetime import datetime
import uuid

rooms = {}

def create_new_room(room_name, password):
    room_id = str(uuid.uuid4())[:8]
    rooms[room_id] = {
        'name': room_name,
        'password': password,
        'files': [],
        'created_at': datetime.now(),
        'members': []
    }
    return room_id

def get_files_in_room(room):
    return room.get('files', [])

def add_file_to_room(room, file_info):
    room_files = get_files_in_room(room)
    room_files.append(file_info)
    room['files'] = room_files

def handle_join_room(room_id, password):
    room = rooms.get(room_id)
    if room and room['password'] == password:
        return room
    return None

def handle_create_room(room_name, password):
    room_id = str(uuid.uuid4())[:8]
    rooms[room_id] = {
        'name': room_name,
        'password': password,
        'files': [],
        'created_at': datetime.now(),
        'members': []
    }
    return room_id

def update_room_info(room_id, file_info):
    room = rooms.get(room_id)
    if room:
        add_file_to_room(room, file_info)
        return True
    return False 