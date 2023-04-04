import config
from utils import ResettableTimer
import collections
import os

class user_cache_data:
    def __init__(self) -> None:
        self.b_need_at = False
        self.needvoice = None
        self.chat_history = collections.deque(maxlen=config.context_length)
        self.chat_prompt_model = 'default'

class user_unstore_cache_data:
    def __init__(self) -> None:
        self.BingAdapter = None


def get_user_cache(history_id):
    if history_id not in user_cache:
        user_cache[history_id] = user_cache_data()
    return user_cache[history_id]

def get_user_unstore_cache(history_id):
    if history_id not in user_unstore_cache:
        user_unstore_cache[history_id] = user_unstore_cache_data()
    return user_unstore_cache[history_id]

def save_cur_multi_chatgpt_prompt_base(sender,group_id,model_name,message):
    with open(f"{cwd_path}\\{config.user_database_path}\\{config.user_prompt_base_path}\\{group_id}_{sender}_{model_name}",
              "w",encoding = 'utf-8') as f:
        f.write(message)
    return

def load_all_multi_chatgpt_prompt_base():
    global cur_multi_chatgpt_prompt_base
    for foldername, subfolders, filenames in os.walk(f"{cwd_path}\\{config.user_database_path}\\{config.user_prompt_base_path}"):
        for filename in filenames:
            with open(f"{cwd_path}\\{config.user_database_path}\\{config.user_prompt_base_path}\\{filename}",
                      "r",encoding = 'utf-8') as f:
                group_user_modelname = filename.split('_',2)
                cur_multi_chatgpt_prompt_base[group_user_modelname[2]] = f.read()
    return

def save_all_user_data():
    import time
    import pickle
    data = pickle.dumps(user_cache)
    time_stamp = int(time.time())
    with open(f"{cwd_path}\\{config.user_database_path}\\{time_stamp}","wb") as f:
        f.write(data)
    with open(f"{cwd_path}\\{config.user_database_path}\\lastdata","wb") as f:
        f.write(data)
    return time_stamp

def load_all_user_data():
    import pickle
    try:
        with open(f"{cwd_path}\\{config.user_database_path}\\lastdata","rb") as f:
            data = pickle.load(f)
    except:
        data = {}
    return data

def init():
    global last_msg_id_of_user, image_gen_messages, is_remote_machine, banned_user_id, \
    is_gpu_connected, ws, gpu_connect_confirm_timer, auth_vip_id, use_chatgpt, billing_chatgpt, \
    admin_setGPT, user_cache, user_unstore_cache, cur_multi_chatgpt_prompt_base, common_chat_history, reg_dirty, \
    cwd_path
    last_msg_id_of_user = {}
    image_gen_messages = []
    is_remote_machine = False
    is_gpu_connected = False
    banned_user_id = set()
    auth_vip_id = config.auth_vip_id
    use_chatgpt = config.use_chatgpt
    billing_chatgpt = config.billing_chatgpt
    cur_multi_chatgpt_prompt_base = config.multi_chatgpt_prompt_base
    common_chat_history = config.common_chat_history
    reg_dirty = config.reg_dirty

    cwd_path = os.getcwd()
    load_all_multi_chatgpt_prompt_base()

    #缓存所有用户的数据
    user_cache = load_all_user_data()
    user_unstore_cache = {}
    admin_setGPT = {"model":"gpt-3.5-turbo"}

    ws = None

    def timer_handler():
        global is_gpu_connected
        is_gpu_connected = False

    gpu_connect_confirm_timer = ResettableTimer(3, timer_handler)
