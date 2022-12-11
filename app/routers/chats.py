from fastapi import APIRouter, UploadFile
import schemas

chats_router = APIRouter(
    prefix = "/chats",
    tags = ["chats"]
)

@chats_router.get('/')
async def get_chats(count: int, offset:int):
    return {'status':'OK'}

@chats_router.post('/')
async def create_chat(chat_data: schemas.ChatCreate):
    return {'status':'OK'}

@chats_router.get('/important')
async def get_important_chats(count: int, offset:int):
    return {'status':'OK'}

@chats_router.post('/important')
async def mark_important_chats(chat_ids: list[int]):
    return {'status':'OK'}

@chats_router.delete('/important')
async def delete_important_chats(chat_ids: list[int]):
    return {'status':'OK'}

@chats_router.get('/messages')
async def get_messages(count: int):
    return {'status':'OK'}

@chats_router.post('/messages')
async def send_message(message: schemas.MessageCreate):
    return {'status':'OK'}

@chats_router.delete('/messages')
async def delete_message(message_ids: list[int], spam: bool, delete_for_all: bool):
    return {'status':'OK'}

@chats_router.get('/messages/important')
async def get_important_messages(count: int, offset:int):
    return {'status':'OK'}

@chats_router.get('/messages/search')
async def get_messages_by_query(count: int, offset:int, query: schemas.MessageSearchQuery):
    return {'status':'OK'}

@chats_router.post('/messages/restore')
async def restore_message(message_ids: list[int]):
    return {'status':'OK'}

@chats_router.patch('/messages/{message_id}')
async def edit_message(message_id: str, message: schemas.MessageCreate):
    return {'status':'OK'}

@chats_router.get('/{chat_id}')
async def get_chat(chat_id:int):
    return {'status':'OK'}

@chats_router.patch('/{chat_id}')
async def edit_chat(chat_id:int, chat_data: schemas.ChatCreate):
    return {'status':'OK'}

@chats_router.delete('/{chat_id}')
async def delete_chat(chat_id:int):
    return {'status':'OK'}

@chats_router.patch('/{chat_id}/join')
async def join_to_chat(chat_id:int):
    return {'status':'OK'}

@chats_router.patch('/{chat_id}/leave')
async def leave_chat(chat_id:int):
    return {'status':'OK'}

@chats_router.put('/{chat_id}/photo')
async def set_chat_photo(chat_id:int, photo: UploadFile):
    return {'status':'OK'}

@chats_router.delete('/{chat_id}/photo')
async def delete_chat_photo(chat_id:int):
    return {'status':'OK'}

@chats_router.get('/{chat_id}/files')
async def get_chat_materials(chat_id:int, count: int, offset:int, media_type: str):
    return {'status':'OK'}

@chats_router.get('/{chat_id}/members')
async def get_chat_members(chat_id:int, count: int, offset:int):
    return {'status':'OK'}

@chats_router.post('/{chat_id}/members')
async def add_chat_members(chat_id:int, user_ids: list[int]):
    return {'status':'OK'}

@chats_router.delete('/{chat_id}/members')
async def delete_chat_members(chat_id:int, users_ids: list[int]):
    return {'status':'OK'}

@chats_router.post('/{chat_id}/messages/pin')
async def pin_message(chat_id:int, message_id: int):
    return {'status':'OK'}

@chats_router.delete('/{chat_id}/messages/pin')
async def unpin_message(chat_id:int, message_id: int):
    return {'status':'OK'}

@chats_router.post('/{chat_id}/messages/important')
async def mark_important_messages(chat_id:int, message_ids: list[int], important: bool):
    return {'status':'OK'}

@chats_router.put('/{chat_id}/messages/mark-as-read')
async def mark_read_messages(chat_id:int, message_ids: list[int]):
    return {'status':'OK'}

@chats_router.get('/{chat_id}/my-role')
async def get_my_role(chat_id:int):
    return {'status':'OK'}

@chats_router.get('/{chat_id}/roles')
async def get_roles(chat_id:int):
    return {'status':'OK'}

@chats_router.post('/{chat_id}/roles')
async def create_role(chat_id:int, role_data: schemas.ChatRole):
    return {'status':'OK'}

@chats_router.patch('/{chat_id}/roles')
async def change_roles(chat_id:int, user_id: int, role_id: int):
    return {'status':'OK'}

@chats_router.patch('/{chat_id}/roles/{role_id}')
async def edit_role(chat_id:int, role_id:int, role_data: schemas.ChatRole):
    return {'status':'OK'}
