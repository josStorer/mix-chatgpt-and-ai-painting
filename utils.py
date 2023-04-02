from threading import Timer

import requests
import io
from PIL import Image

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


def get_history_id(group_id, sender):
    if shared_context:
        return str(group_id)
    return str(group_id) + '_' + str(sender)


def gen_image(sender, gen_message, group_id):
    real_payload = default_gen.copy()
    real_payload.update(gen_message)
    if real_payload["steps"] > max_step:
        real_payload["steps"] = max_step
        at_user_in_group(sender, sender, f"最大steps被限制为{max_step}, 现以{max_step}开始生成", group_id)

    try:
        response = requests.post(url=f'{gpu_url}{gpu_api_path}', json=real_payload)
    except Exception as e:
        if "Connection refused" in str(e):
            raise Exception(gpu_disconnected_msg)
        raise e

    if response.status_code == 503:
        raise Exception(gpu_disconnected_msg)

    r = response.json()

    image = r['images'][0].split(",", 1)[0]
    image_info = json.loads(r["info"])
    return image, image_info["seed"], real_payload["prompt"]

def b64_img(image: Image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = 'data:image/png;base64,' + str(base64.b64encode(buffered.getvalue()), 'utf-8')
    return img_base64


def gen_img2img(sender, gen_message, group_id):
    real_payload = gen_param.copy()
    init_images = []
    width, height = None,None
    for img_url in gen_message["img_urls"]:
        try:
            print (f"img_url : {img_url}")
            response = requests.get(url=f'{img_url}')
            img = Image.open(io.BytesIO(response.content)) # .convert("RGB")
            width, height = img.width, img.height
            init_images.append(b64_img(img))
        except Exception as e:
            raise e
    # real_payload.update(gen_message)
    real_payload["init_images"] = init_images
    # 对超过1024像素的进行等比例缩放
    import math
    max_axis = max(width,height)
    if max_axis > 1024:
        width = math.floor(1024.0 / max_axis * width)
        height = math.floor(1024.0 / max_axis * height)
    real_payload["width"] = width
    real_payload["height"] = height
    if real_payload["steps"] > max_step:
        real_payload["steps"] = max_step
        at_user_in_group(sender, sender, f"最大steps被限制为{max_step}, 现以{max_step}开始生成", group_id)
    try:
        # print (f"real_payload : {real_payload}")
        response = requests.post(url=f'{gpu_url}{gpu_api_img}', json=real_payload)
    except Exception as e:
        if "Connection refused" in str(e):
            raise Exception(gpu_disconnected_msg)
        raise e
    r = response.json()
    print (f"get img from api {r}")

    image = r['images'][0].split(",", 1)[0]
    image_info = json.loads(r["info"])
    return image, image_info["seed"], real_payload["prompt"]


def at_user_in_group(message_source, at_user_id, text, group_id, bCleaned = False, Prefix = ""):
    # if text == "权限不足":
    #     return
    history_id = get_history_id(group_id, at_user_id)
    send_message_to_group(message_source, f"{Prefix}[CQ:at,qq={at_user_id}]\n{text}", group_id, bCleaned)

def at_user_in_group_with_voice(message_source, at_user_id, text, group_id, bCleaned = False, Prefix = ""):
    # if text == "权限不足":
    #     return
    history_id = get_history_id(group_id, at_user_id)
    if global_var.get_user_cache(history_id).needvoice:
        send_record_to_group(message_source, f"{Prefix}[CQ:at,qq={at_user_id}]\n{text}", group_id, global_var.get_user_cache(history_id).needvoice, Prefix = Prefix)
        return

    send_message_to_group(message_source, f"{Prefix}[CQ:at,qq={at_user_id}]\n{text}", group_id, bCleaned)


def send_err_to_group(message_source, e, group_id):
    import traceback
    traceback.print_exc()
    send_message_to_group(message_source, f"[CQ:at,qq={message_source}]\n错误:\n{str(e) if str(e) != '' else e.message}", group_id)

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
