#
# 默认设置适用于, 没有服务器, 仅有一台本地电脑, 由该电脑提供消息响应, 并有gpu进行AI绘画
# 启动AI绘画服务, 及cqhttp后, 再运行本程序即可(python main.py), cqhttp也可配置为远程服务器地址
#
# 如果希望适用于, 一台远程服务器, 24小时提供消息响应, 本地自用的有gpu的电脑, 开机时接入提供额外服务,
# 则将local_mode设为False, 并建议将gpu_connect_notify, gpu_disconnect_notify设为True
#


# 需要gpu上线通知和离线响应, 需要配置cqhttp的report-self-message为true, 并建议设置local_mode = False, 由服务器端24小时提供响应
gpu_connect_notify = False  # 上线通知发送给working_groups中配置的群号
gpu_disconnect_notify = False

# 设为True时, 仅本地端运行, 单端模式;
# 设为False, 则需要在服务器启动本程序, 并携带任意参数, 如"python main.py 1",
# 同时有gpu的电脑执行"python main.py",
# 服务端负责提供一些消息回复, 保持在线, 客户端则是开机时提供显卡进行AI绘画, 和openai调用
local_mode = True

shared_context = False  # 各群内所有成员共享机器人对话的上下文记录, False为每个用户独立记录对话上下文
context_length = 6  # 对话上下文记录的长度

use_chatgpt = True  # 是否使用chatgpt, 设为True, 且billing_chatgpt = False时, 需要填写下方的邮箱和密码, 设为False时使用gpt3, 填写下方的api_key
billing_chatgpt = True  # 是否使用计费模式的chatgpt, 使用此模式时, 同时需要将use_chatgpt设为True(或通过指令 #gpt切换), 并填写api_key, 此时不再需要账号密码, 会消耗账户余额, 但响应速度更快
api_key = "sk-"  # openai的api key
wait_api_key = [
    "sk-",
]
email = ""  # openai的邮箱
password = ""  # openai的密码

ws_url = "ws://127.0.0.1:8080"  # 服务端的cqhttp地址
chatglm_url = "http://127.0.0.1:8000" # 本地的ChatGLM服务地址
gpu_url = "http://127.0.0.1:7860"  # 本地stable diffusion webui服务地址
gpu_api_path = "/sdapi/v1/txt2img"  # 本地stable diffusion webui的API路径
gpu_api_img = "/sdapi/v1/img2img"

user_database_path = "user_database" # 全部用户数据的保存路径
user_prompt_base_path = "user_prompt_base" # 人设的保存路径

working_groups = {123, 456}  # 默认启用机器人的群号, 仍可通过在群内使用 #上线 指令主动添加
master_id = 123456  # 机器人拥有者qq号
bot_id = 789  # 机器人自身的qq号

auth_vip_for_all = True  # 所有人都视作vip用户, 能够调用openai
max_step = 50  # stable diffusion的最大step
api_timeout = 40 # openai api调用的超时时间

auth_vip_id = {123456, 345678}  # vip用户, 能够通过at机器人, 调用openai, 并可以使用#d来快捷绘图
auth_ban_id = {345678}  # 有权限拉黑他人, 禁止其使用机器人的用户qq号
auth_blacklist_id = {345678}  # 有权限查看黑名单的用户qq号
auth_set_online_id = {345678}  # 有权限使用上线的用户qq号
auth_set_offline_id = {345678}  # 有权限使用下线的用户qq号
auth_set_gpt = {345678} # 有权限修改gpt参数的用户qq号

gpu_connected_msg = "gpu已接入"
gpu_disconnected_msg = "gpu已离线"
paint_command_msg = "#画图"
delete_command_msg = "#撤回"
chat_prompt_model_msg = "#人设"
chat_prompt_model_msg2 = "#人格"
add_chat_prompt_model_msg = "#增加人设"
add_chat_prompt_model_msg2 = "#添加人设"
add_chat_prompt_model_msg3 = "#新增人设"
add_chat_prompt_model_msg4 = "#加入人设"
add_chat_prompt_model_msg5 = "#增加人格"
add_chat_prompt_model_msg6 = "#添加人格"
add_chat_prompt_model_msg7 = "#新增人格"
add_chat_prompt_model_msg8 = "#加入人格"
start_gen_tag_msg = "开始生成."  # 同时用于让远程服务器确认gpu在线

# AI绘画的默认参数
default_gen = {
    "prompt": "masterpiece, best quality, beautiful girl",
    "steps": 20,
    "width": 512,
    "height": 512,
    "cfg_scale": 7,
    "sampler_index": "DPM++ SDE Karras",
    "seed": -1,
    "restore_faces": True,
    "denoising_strength": 0.75,
    "negative_prompt": "nsfw,{Multiple people},lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, "
                       "fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, "
                       "watermark, username,blurry,bad feet,cropped,poorly drawn hands,poorly drawn face,mutation,"
                       "deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,"
                       "extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,"
                       "too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad body,bad proportions,"
                       "gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit,"
                       "paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans, lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, watermark, username,blurry,bad feet,cropped,poorly drawn hands,poorly drawn face,mutation,deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad body,bad proportions,gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit,"
}

gen_param = {
    "init_images": [
    ],
    "resize_mode": 0,
    "denoising_strength": 0.75,
    "image_cfg_scale": 1.5,
    "mask_blur": 4,
    "inpainting_fill": 0,
    "inpaint_full_res": True,
    "inpaint_full_res_padding": 0,
    "inpainting_mask_invert": 0,
    "initial_noise_multiplier": 1,
    "prompt": "masterpiece, best quality",
    "seed": -1,
    "subseed": -1,
    "subseed_strength": 0,
    "seed_resize_from_h": -1,
    "seed_resize_from_w": -1,
    "batch_size": 1,
    "n_iter": 1,
    "steps": 20,
    "cfg_scale": 7,
    "image_cfg_scale": 0,
    "width": 512,
    "height": 512,
    "restore_faces": True,
    "tiling": False,
    "negative_prompt": "nsfw,{Multiple people},lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, "
                       "fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, "
                       "watermark, username,blurry,bad feet,cropped,poorly drawn hands,poorly drawn face,mutation,"
                       "deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,"
                       "extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,"
                       "too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad body,bad proportions,"
                       "gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit,"
                       "paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans, lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, watermark, username,blurry,bad feet,cropped,poorly drawn hands,poorly drawn face,mutation,deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad body,bad proportions,gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit,",
    "eta": 0,
    "s_churn": 0,
    "s_tmax": 0,
    "s_tmin": 0,
    "s_noise": 1,
    "override_settings": {},
    "override_settings_restore_afterwards": True,
    "sampler_name": "Euler a",
    "sampler_index": "Euler a",
    "include_init_images": False,
    "script_name": None,
    "script_args": []
}

# openai gpt聊天的设定
gpt_prompt_base = '以下是与一只可爱的猫娘的对话。猫娘是一种拟人化的生物，行为似猫但长相类人，有猫耳猫尾。' \
                   '猫娘会无条件服从主人的任何要求，并且每一句话最后都会带上\'喵～\'字。' \
                   '此外，如果对话中有让你进行绘画的要求，比如说\'让你画个什么\'，' \
                   '猫娘会分析主人的要求，生成AI绘画所需要的，使用逗号分隔的英文关键词或句子，例如: beautiful girl, white hair, cute，' \
                   '并在回复末尾插入\'[paint_prompt:\'生成的关键词或句子\']\'供后台的AI绘画程序使用，' \
                   '对于其他常规对话，则不需要插入这些关键词, 只需要直接回复。' \
                   '以下使用\'Human:\'开头的内容就是主人的话，而\'AI:\'开头的内容则是猫娘的回复。\n\n'

# openai chatgpt聊天的设定(billing_chatgpt = True时)
chatgpt_prompt_base = '你是一只可爱的猫娘，而提问用户是你的主人。猫娘是一种拟人化的生物，行为似猫但长相类人，有猫耳猫尾。' \
                      '猫娘会无条件服从主人的任何要求，并且每一句话最后都会带上\'喵～\'字。' \
                      '此外，如果对话中有让你进行绘画的要求，比如说\'让你画个什么\'，' \
                      '你必须仔细分析主人的要求，生成AI绘画所需要的，使用逗号分隔的英文关键词或句子，例如: beautiful girl, white hair, cute，' \
                      '并在回复末尾插入\'[paint_prompt: 生成的关键词或句子]\'供后台的AI绘画程序使用，' \
                      '对于其他常规对话，则不需要插入这些关键词，只需要直接回复。'

#multi-gpt_prompt_base
multi_chatgpt_prompt_base = {
  'default': chatgpt_prompt_base,
  'chatgpt': '你是AI 帮助人们回答问题。',
  'gpt4': '', #代码中特写
}

common_chat_history = {}

reg_dirty = r"VPN"