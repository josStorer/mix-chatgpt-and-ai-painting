import config
from utils import ResettableTimer


def init():
    global last_msg_id_of_user, image_gen_messages, is_remote_machine, banned_user_id, \
    is_gpu_connected, ws, gpu_connect_confirm_timer, auth_vip_id, use_chatgpt, billing_chatgpt, \
    chat_history, user_needat, user_needvoice, admin_setGPT
    last_msg_id_of_user = {}
    image_gen_messages = []
    is_remote_machine = False
    is_gpu_connected = False
    banned_user_id = set()
    auth_vip_id = config.auth_vip_id
    use_chatgpt = config.use_chatgpt
    billing_chatgpt = config.billing_chatgpt
    chat_history = {}

    user_needat = {}
    user_needvoice = {}
    admin_setGPT = {"model":"gpt-3.5-turbo"}

    ws = None

    def timer_handler():
        global is_gpu_connected
        is_gpu_connected = False

    gpu_connect_confirm_timer = ResettableTimer(3, timer_handler)
