import json

import global_var


def get_guild_bot_id():
    global_var.ws.send(json.dumps({
        "action": "get_guild_service_profile",
        "params": {},
        "echo": {
            "type": "guild_bot_id"
        }
    }))


def send_message_to_group(message_source, message, group_id):
    global_var.ws.send(json.dumps({
        "action": "send_group_msg",
        "params": {
            "group_id": str(group_id),
            "message": message
        },
        "echo": {
            "message_source": message_source
        }
    }))


def send_message_to_channel(message_source, message, guild_id, channel_id):
    global_var.ws.send(json.dumps({
        "action": "send_guild_channel_msg",
        "params": {
            "guild_id": str(guild_id),
            "channel_id": str(channel_id),
            "message": message
        },
        "echo": {
            "message_source": message_source
        }
    }))


def delete_msg(msg_id):
    global_var.ws.send(json.dumps({
        "action": "delete_msg",
        "params": {
            "message_id": msg_id,
        }
    }))
