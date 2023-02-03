from db_client import DBClient
from tests.conftest import TEST_DB_URL


def test_write_to_db_command(db_connection):
	command = """ 
	INSERT INTO Users(id, username, chat_id) VALUES(?, ?, ?); 
	"""
	id = 1
	username = 'Viposha'
	chat_id = 123456
	client = DBClient(TEST_DB_URL)
	client.create_conn()
	client.execute_command_params(command, (id, username, chat_id))
	cursor = db_connection.cursor()
	cursor.execute("""SELECT * FROM Users;""")
	users = cursor.fetchall()
	assert len(users) == 1
	user = users[0]
	assert user[0] == id
	assert user[1] == username
	assert user[2] == chat_id


def test_read_from_db_client(db_connection):
	id = 1
	username = 'Viposha'
	chat_id = 123456
	db_connection.execute("""INSERT INTO Users(id, username,chat_id) VALUES(?, ?, ?);""", (id, username, chat_id))
	db_connection.commit()
	command = """SELECT * FROM Users;"""
	client = DBClient(TEST_DB_URL)
	client.create_conn()
	users = client.execute_select_command(command)
	assert len(users) == 1
	user = users[0]
	assert user[0] == id
	assert user[1] == username
	assert user[2] == chat_id


# def test_extract():
#
# 	mess = {'content_type': 'text', 'id': 632, 'message_id': 632, 'from_user': {'id': 482085376, 'is_bot': False, 'first_name': 'Vitalii', 'username': 'Viposha', 'last_name': 'Hoshchenko', 'language_code': 'uk', 'can_join_groups': None, 'can_read_all_group_messages': None, 'supports_inline_queries': None, 'is_premium': None, 'added_to_attachment_menu': None}, 'date': 1675247875, 'chat': {'id': 482085376, 'type': 'private', 'title': None, 'username': 'Viposha', 'first_name': 'Vitalii', 'last_name': 'Hoshchenko', 'is_forum': None, 'photo': None, 'bio': None, 'join_to_send_messages': None, 'join_by_request': None, 'has_private_forwards': None, 'has_restricted_voice_and_video_messages': None, 'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None, 'slow_mode_delay': None, 'message_auto_delete_time': None, 'has_protected_content': None, 'sticker_set_name': None, 'can_set_sticker_set': None, 'linked_chat_id': None, 'location': None, 'active_usernames': None, 'emoji_status_custom_emoji_id': None}, 'sender_chat': None, 'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_sender_name': None, 'forward_date': None, 'is_automatic_forward': None, 'reply_to_message': None, 'via_bot': None, 'edit_date': None, 'has_protected_content': None, 'media_group_id': None, 'author_signature': None, 'text': 'qqq', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'reply_markup': None, 'message_thread_id': None, 'is_topic_message': None, 'forum_topic_created': None, 'forum_topic_closed': None, 'forum_topic_reopened': None, 'json': {'message_id': 632, 'from': {'id': 482085376, 'is_bot': False, 'first_name': 'Vitalii', 'last_name': 'Hoshchenko', 'username': 'Viposha', 'language_code': 'uk'}, 'chat': {'id': 482085376, 'first_name': 'Vitalii', 'last_name': 'Hoshchenko', 'username': 'Viposha', 'type': 'private'}, 'date': 1675247875, 'text': 'qqq'}}
#
# 	assert extract(mess) == 'Viposha', 482085376
