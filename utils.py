from threading import Timer

import requests

from config import *
from ws_wrapper import *
import global_var


def is_group_online(group_id):
    return group_id in working_groups


def is_user_banned(user_id):
    return user_id in global_var.banned_user_id


def is_vip(user_id):
    return auth_vip_for_all or user_id in global_var.auth_vip_id


def is_remote_machine():
    return local_mode or global_var.is_remote_machine


def is_not_remote_machine():
    return local_mode or not global_var.is_remote_machine


def get_sender_key_in_group(group_id, sender):
    if shared_context:
        return str(group_id)
    return str(group_id) + '_' + str(sender)


def gen_image(sender, gen_message, group_id, channel_id, is_guild):
    real_payload = default_gen.copy()
    real_payload.update(gen_message)
    if real_payload["steps"] > max_step:
        real_payload["steps"] = max_step
        at_user_in_group(sender, sender, f"最大steps被限制为{max_step}, 现以{max_step}开始生成", group_id, channel_id,
                         is_guild)

    try:
        response = requests.post(url=f'{gpu_url}{gpu_api_path}', json=real_payload)
    except Exception as e:
        if "Connection refused" in str(e):
            raise Exception(gpu_disconnected_msg)
        raise e

    if response.status_code == 503:
        raise Exception(gpu_disconnected_msg)

    if response.status_code != 200:
        raise Exception(str(response.status_code) + ": " + response.text)

    r = response.json()

    image = r['images'][0].split(",", 1)[0]
    image_info = json.loads(r["info"])
    return image, image_info["seed"], real_payload["prompt"]


# is_guild是冗余参数, 实际上判断channel_id就知道是否是频道, 未来有需要添加新参数时, 可以全局搜索替换成其他的, 一把梭已经成屎山了, 出此下策QAQ, 二十年后有空了就重构
def at_user_in_group(message_source, at_user_id, text, group_id, channel_id, is_guild: bool):
    message = f"[CQ:at,qq={at_user_id}]\n{text}"
    if is_guild:
        send_message_to_channel(message_source, message, group_id, channel_id)
    else:
        send_message_to_group(message_source, message, group_id)


def send_err_to_group(message_source, e, group_id, channel_id, is_guild: bool):
    at_user_in_group(message_source, message_source, f"错误:\n{str(e) if str(e) != '' else e.message}", group_id,
                     channel_id, is_guild)


class ResettableTimer(object):
    def __init__(self, interval, function):
        self.interval = interval
        self.function = function
        self.timer = Timer(self.interval, self.function)

    def run(self):
        try:
            self.timer.start()
        except:
            pass

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.interval, self.function)
