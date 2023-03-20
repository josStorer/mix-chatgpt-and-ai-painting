import config
from utils import ResettableTimer
import collections

class user_cache_data:
    def __init__(self) -> None:
        self.b_need_at = False
        self.needvoice = None
        self.chat_history = collections.deque(maxlen=config.context_length)

def get_user_cache(history_id):
    if history_id not in user_cache:
        user_cache[history_id] = user_cache_data()
    return user_cache[history_id]

def init():
    global last_msg_id_of_user, image_gen_messages, is_remote_machine, banned_user_id, \
    is_gpu_connected, ws, gpu_connect_confirm_timer, auth_vip_id, use_chatgpt, billing_chatgpt, \
    admin_setGPT, user_cache
    last_msg_id_of_user = {}
    image_gen_messages = []
    is_remote_machine = False
    is_gpu_connected = False
    banned_user_id = set()
    auth_vip_id = config.auth_vip_id
    use_chatgpt = config.use_chatgpt
    billing_chatgpt = config.billing_chatgpt

    #缓存所有用户的数据
    user_cache = {}
    admin_setGPT = {"model":"gpt-3.5-turbo"}

    ws = None

    def timer_handler():
        global is_gpu_connected
        is_gpu_connected = False

    gpu_connect_confirm_timer = ResettableTimer(3, timer_handler)
