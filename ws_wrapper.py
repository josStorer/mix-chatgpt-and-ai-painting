import json

import global_var


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


def delete_msg(msg_id):
    global_var.ws.send(json.dumps({
        "action": "delete_msg",
        "params": {
            "message_id": msg_id,
        }
    }))
