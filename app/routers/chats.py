from fastapi import APIRouter

chats_router = APIRouter(
    prefix = "/chats",
    tags = ["chats"]
)

@chats_router.get('/')
async def get_chats():
    pass

@chats_router.post('/')
async def create_chat():
    pass

@chats_router.get('/important')
async def get_important_chats():
    pass

@chats_router.post('/important')
async def mark_important_chats():
    pass

@chats_router.delete('/important')
async def delete_important_chats():
    pass

@chats_router.get('/messages')
async def get_messages():
    pass

@chats_router.post('/messages')
async def send_message():
    pass

@chats_router.delete('/messages')
async def delete_message():
    pass

@chats_router.get('/messages/important')
async def get_important_messages():
    pass

@chats_router.get('/messages/search')
async def get_messages_by_query():
    pass

@chats_router.post('/messages/restore')
async def restore_message():
    pass

@chats_router.patch('/messages/{message_id}')
async def edit_message(message_id: str):
    pass

@chats_router.get('/{chat_id}')
async def get_chat(chat_id:int):
    pass

@chats_router.patch('/{chat_id}')
async def edit_chat(chat_id:int):
    pass

@chats_router.delete('/{chat_id}')
async def delete_chat(chat_id:int):
    pass

@chats_router.patch('/{chat_id}/join')
async def join_to_chat(chat_id:int):
    pass

@chats_router.patch('/{chat_id}/leave')
async def leave_chat(chat_id:int):
    pass

@chats_router.put('/{chat_id}/photo')
async def set_chat_photo(chat_id:int):
    pass

@chats_router.delete('/{chat_id}/photo')
async def delete_chat_photo(chat_id:int):
    pass

@chats_router.get('/{chat_id}/files')
async def get_chat_materials(chat_id:int):
    pass

@chats_router.get('/{chat_id}/members')
async def get_chat_members(chat_id:int):
    pass

@chats_router.post('/{chat_id}/members')
async def add_chat_members(chat_id:int):
    pass

@chats_router.delete('/{chat_id}/members')
async def delete_chat_members(chat_id:int):
    pass

@chats_router.post('/{chat_id}/messages/pin')
async def pin_message(chat_id:int):
    pass

@chats_router.delete('/{chat_id}/messages/pin')
async def unpin_message(chat_id:int):
    pass

@chats_router.post('/{chat_id}/messages/important')
async def mark_important_messages(chat_id:int):
    pass

@chats_router.put('/{chat_id}/messages/mark_as_read')
async def mark_read_messages(chat_id:int):
    pass

@chats_router.get('/{chat_id}/my_role')
async def get_my_role(chat_id:int):
    pass

@chats_router.get('/{chat_id}/roles')
async def get_roles(chat_id:int):
    pass

@chats_router.post('/{chat_id}/roles')
async def create_role(chat_id:int):
    pass

@chats_router.patch('/{chat_id}/roles')
async def change_roles(chat_id:int):
    pass

@chats_router.patch('/{chat_id}/roles/{role_id}')
async def edit_role(chat_id:int, role_id:int):
    pass
