import config
from utils import ResettableTimer


def init():
    global last_msg_id_of_user, image_gen_messages, is_remote_machine, banned_user_id, is_gpu_connected
    global ws, gpu_connect_confirm_timer, auth_vip_id, use_chatgpt, chat_history, users_not_need_at
    last_msg_id_of_user = {}
    image_gen_messages = []
    is_remote_machine = False
    is_gpu_connected = False
    banned_user_id = set()
    auth_vip_id = config.auth_vip_id
    use_chatgpt = config.use_chatgpt
    chat_history = {}
    users_not_need_at = {}

    ws = None

    def timer_handler():
        global is_gpu_connected
        is_gpu_connected = False

    gpu_connect_confirm_timer = ResettableTimer(3, timer_handler)
