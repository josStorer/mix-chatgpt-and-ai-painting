from utils import *
from ws_wrapper import *
import global_var


def operation_general_response(sender, message, group_id):
    at_user_in_group(sender, sender,
                     "收到" + (", 我的主人, 您的消息是: " if sender == master_id else "") + message
                     .replace("&#91;", "[")
                     .replace("&#93;", "]"), group_id)


def operation_set_online(sender, _, group_id):
    if sender == master_id or sender in auth_set_online_id:
        working_groups.add(group_id)
        if is_remote_machine():
            global_var.is_gpu_connected = True
            global_var.gpu_connect_confirm_timer.reset()
            at_user_in_group(sender, sender, "主人, 我已上线", group_id)
    else:
        if is_remote_machine():
            at_user_in_group(sender, sender, "权限不足", group_id)


def operation_set_offline(sender, _, group_id):
    if sender == master_id or sender in auth_set_offline_id:
        working_groups.remove(group_id)
        if is_remote_machine():
            at_user_in_group(sender, sender, "再见, 主人QAQ", group_id)
    else:
        if is_remote_machine():
            at_user_in_group(sender, sender, "权限不足", group_id)


def operation_gen_image(sender, message, group_id):
    new_message = message
    if new_message.startswith("#d"):
        if is_vip(sender):
            new_message = new_message.replace("#d", "")
            if is_group_online(group_id):
                global_var.gpu_connect_confirm_timer.run()
                if is_not_remote_machine():
                    at_user_in_group(sender, sender,
                                     f"尊贵的vip用户, 检测到您已进行了py交易, 支持使用额外指令, 现已为您{start_gen_tag_msg}",
                                     group_id)
        else:
            if is_remote_machine():
                operation_general_response(sender, message, group_id)
            return
    else:
        if is_group_online(group_id):
            global_var.gpu_connect_confirm_timer.run()
            if is_not_remote_machine():
                at_user_in_group(sender, sender, f"收到, {start_gen_tag_msg}", group_id)

    new_message = new_message.replace(paint_command_msg, "")
    new_message = new_message.strip()
    if len(new_message) == 0:
        global_var.image_gen_messages.append(({}, sender, group_id, False))
    elif new_message[0] == '{':
        try:
            obj = json.loads(new_message)
            global_var.image_gen_messages.append((obj, sender, group_id, False))
        except Exception as e:
            if is_remote_machine():
                send_err_to_group(sender, e, group_id)
    else:
        try:
            res = new_message.replace(";", ".")
            if res.count(".") > 2:
                res = res.split('.', 3)
            else:
                res = [res,]
            new_message = res[-1]
            res_len = len(res)
            seed, steps, w, h = None, None, None, None
            if res_len >= 2:
                wh = res[0].split("x", 1)
                w = wh[0]
                if len(wh) > 1:
                    h = wh[1]
            if res_len >= 3:
                steps = res[1]
            if res_len >= 4:
                seed = res[2]

            gen_message = default_gen.copy()
            if len(new_message) != 0:
                gen_message["prompt"] = new_message
            if steps is not None and len(steps) != 0:
                gen_message["steps"] = int(steps)
            if seed is not None and len(seed) != 0:
                gen_message["seed"] = int(seed)
            if w is not None and len(w) != 0:
                gen_message["width"] = int(w)
            if h is not None and len(h) != 0:
                gen_message["height"] = int(h)

            global_var.image_gen_messages.append((gen_message, sender, group_id, False))
        except Exception as e:
            if is_remote_machine():
                send_err_to_group(sender, e, group_id)


def operation_delete_msg(sender, _, group_id):
    delete_msg(global_var.last_msg_id_of_user[sender])


def operation_help(sender, _, group_id):
    send_message_to_group(sender, f'''机器人使用说明:
#消息
 - 支持转换CQ消息原始数据, 外网服务器可借此拉取外网资源

{paint_command_msg}+描述
 - {paint_command_msg}后直接连接关键词, 进行快捷绘图
 - e.g. {paint_command_msg}girls

{paint_command_msg}+宽度x高度.步数.种子.描述
 - 快捷配置绘图, 点号间可为空使用默认值, 点号与分号可混用
 - e.g. {paint_command_msg}128x128.10.2556931196.girls

{paint_command_msg}{"{}"}
 - 花括号内传入标准json数据控制绘画, 支持字段prompt,steps,width,height,cfg_scale,sampler_index,seed,negative_prompt
 - 输入#默认, 以查看示例

{delete_command_msg}
 - 撤回上一条由你触发的机器人消息

#默认
 - 查看画图的默认配置

更多指令如下
{both_operations.keys()}
''', group_id)


def operation_default_config(sender, _, group_id):
    send_message_to_group(sender, json.dumps(default_gen, indent=2), group_id)


def operation_set_banned(sender, message, group_id):
    if sender == master_id or sender in auth_ban_id:
        new_message = message.replace("#拉黑", "")
        user = int(new_message)
        if user != master_id:
            global_var.banned_user_id.add(user)
            if is_remote_machine():
                at_user_in_group(sender, sender, "拉黑成功", group_id)
        else:
            if is_remote_machine():
                at_user_in_group(sender, sender, "我怎么可能拉黑我最爱的主人呢???!!!", group_id)
    else:
        if is_remote_machine():
            at_user_in_group(sender, sender, "权限不足", group_id)


def operation_remove_banned(sender, message, group_id):
    if sender == master_id or sender in auth_ban_id:
        new_message = message.replace("#解除", "")
        user = int(new_message)
        global_var.banned_user_id.remove(user)
        if is_remote_machine():
            at_user_in_group(sender, sender, "解除黑名单成功", group_id)
    else:
        if is_remote_machine():
            at_user_in_group(sender, sender, "权限不足", group_id)


def operation_show_blacklist(sender, _, group_id):
    if sender == master_id or sender in auth_blacklist_id:
        at_user_in_group(sender, sender, "黑名单:\n" + str(global_var.banned_user_id), group_id)
    else:
        at_user_in_group(sender, sender, "权限不足", group_id)


def operation_add_vip(sender, message, group_id):
    if sender == master_id:
        new_message = message.replace("#vip", "")
        user = int(new_message)
        global_var.auth_vip_id.add(user)
        if is_remote_machine():
            at_user_in_group(sender, sender, f"新增vip: {user}", group_id)
    else:
        if is_remote_machine():
            at_user_in_group(sender, sender, "权限不足", group_id)


def operation_remove_vip(sender, message, group_id):
    if sender == master_id:
        new_message = message.replace("#unvip", "")
        user = int(new_message)
        global_var.auth_vip_id.remove(user)
        if is_remote_machine():
            at_user_in_group(sender, sender, f"移除vip: {user}", group_id)
    else:
        if is_remote_machine():
            at_user_in_group(sender, sender, "权限不足", group_id)


def operation_switch_gpt(sender, message, group_id):
    if sender == master_id:
        global_var.use_chatgpt = not global_var.use_chatgpt
        print("use_chatgpt:", global_var.use_chatgpt)
        if is_not_remote_machine():
            at_user_in_group(sender, sender, "已切换至chatGPT" if global_var.use_chatgpt else "已切换至GPT3", group_id)
    else:
        if is_remote_machine():
            at_user_in_group(sender, sender, "权限不足", group_id)

def operation_switch_gpt35(sender, message, group_id):
    if sender == master_id:
        global_var.billing_chatgpt = not global_var.billing_chatgpt
        print("billing_chatgpt:", global_var.billing_chatgpt)
        if is_not_remote_machine():
            at_user_in_group(sender, sender, "已切换至GPT3.5 Turbo" if global_var.billing_chatgpt else "已切换至ChatGPT", group_id)
    else:
        if is_remote_machine():
            at_user_in_group(sender, sender, "权限不足", group_id)


def operation_clear_chat(sender, message, group_id):
    if global_var.is_remote_machine:
        return

    history_id = get_history_id(group_id, sender)
    if len(global_var.get_user_cache(history_id).chat_history) == 0:
        at_user_in_group(sender, sender, "没有可以清理的对话", group_id)
        return

    if shared_context:
        if sender == master_id:
            global_var.get_user_cache(history_id).chat_history.clear()
            at_user_in_group(sender, sender, "已清理群内共享对话上下文", group_id)
        else:
            at_user_in_group(sender, sender, "权限不足", group_id)
    else:
        global_var.get_user_cache(history_id).chat_history.clear()
        at_user_in_group(sender, sender, "已清理你的对话上下文", group_id)


def operation_switch_at(sender, message, group_id):
    if global_var.is_remote_machine:
        return

    history_id = get_history_id(group_id, sender)
    user_cache = global_var.get_user_cache(get_history_id(group_id, sender))
    if not user_cache.b_need_at:
        user_cache.b_need_at = True
        at_user_in_group(sender, sender, "已无需at即可对话", group_id)
        return

    user_cache.b_need_at = False
    at_user_in_group(sender, sender, "恢复到需要at再进行对话", group_id)

def operation_switch_voice(sender, message, group_id):
    if global_var.is_remote_machine:
        return

    history_id = get_history_id(group_id, sender)
    if not global_var.get_user_cache(history_id).needvoice:
        at_user_in_group(sender, sender, "检测到还没有开启语音对话。已开启语音对话。\n" \
                         "提示：语音功能一共有3个指令，#语音切换，#音色切换，#朗读+[需要朗读的文案]", group_id)
        global_var.get_user_cache(history_id).needvoice = 4
        return

    global_var.get_user_cache(history_id).needvoice = None
    at_user_in_group(sender, sender, "恢复到文本对话", group_id)

def operation_switch_sound(sender, message, group_id):
    if global_var.is_remote_machine:
        return

    history_id = get_history_id(group_id, sender)
    if not global_var.get_user_cache(history_id).needvoice:
        operation_switch_voice(sender, message, group_id)
        return

    speaker_dict = {
        0:"綾地寧々放送です",
        1:"ありはら ななみ放送です",
        2:"现在是小茸与您对话",
        3:"现在是唐乐吟与您对话",
        4:"现在是锦木千束与您对话",
        5:"现在是刻晴与您对话",
        6:"现在是优菈与您对话",
        7:"现在是派蒙与您对话"
    }
    global_var.get_user_cache(history_id).needvoice = (global_var.get_user_cache(history_id).needvoice + 1) % len(speaker_dict)
    needvoice = global_var.get_user_cache(history_id).needvoice
    if global_var.get_user_cache(history_id).needvoice in [0,1]:
        send_record_to_group_jp(sender, f"{speaker_dict[needvoice]}", group_id, needvoice)
    else:
        send_record_to_group(sender, f"{speaker_dict[needvoice]}", group_id, needvoice)

def operation_voice(sender, message, group_id):
    message = message.replace("#朗读 ","")
    history_id = get_history_id(group_id, sender)
    if not global_var.get_user_cache(history_id).needvoice:
        operation_switch_voice(sender, message, group_id)
        return
    send_record_to_group(sender, f"{message}", group_id, global_var.get_user_cache(history_id).needvoice)
    return

def operation_switch_model(sender, message, group_id):
    if global_var.is_remote_machine:
        return

    if sender != master_id:
        at_user_in_group(sender, sender, "权限不足", group_id)
        return

    new_message = message.replace("#model", "")
    new_message = new_message.strip()

    response = requests.get(f"{gpu_url}/sdapi/v1/sd-models")

    if response.status_code == 200:
        models = [model["title"] for model in response.json()]
    else:
        at_user_in_group(sender, sender, "获取模型列表失败", group_id)
        return

    try:
        options = requests.get(f"{gpu_url}/sdapi/v1/options").json()
        if new_message == "":
            at_user_in_group(
                sender, sender, f"当前激活模型:\n{options['sd_model_checkpoint']}\n\n当前可用模型:\n" + "\n".join(models), group_id)
        else:
            for model_title in models:
                if new_message.lower() in model_title.lower():
                    options['sd_model_checkpoint'] = model_title
                    requests.post(f"{gpu_url}/sdapi/v1/options", json=options)
                    at_user_in_group(sender, sender, f"已切换至模型:\n{model_title}", group_id)
                    return
            at_user_in_group(sender, sender, "未找到匹配的模型", group_id)
    except Exception as e:
        send_err_to_group(sender, e, group_id)
        return


def operation_switch_vae(sender, message, group_id):
    if global_var.is_remote_machine:
        return

    if sender != master_id:
        at_user_in_group(sender, sender, "权限不足", group_id)
        return

    new_message = message.replace("#vae", "")
    new_message = new_message.strip()

    try:
        options = requests.get(f"{gpu_url}/sdapi/v1/options").json()
        if new_message == "":
            at_user_in_group(sender, sender, f"当前激活VAE:\n{options['sd_vae']}", group_id)
        else:
            old_vae = options['sd_vae']
            options['sd_vae'] = new_message
            requests.post(f"{gpu_url}/sdapi/v1/options", json=options)
            at_user_in_group(
                sender, sender, f"已尝试切换VAE, 注意VAE切换必须准确匹配名称\n如果出现效果异常, 可能是切换错误\n可切换回先前的VAE:\n{old_vae}", group_id)
    except Exception as e:
        send_err_to_group(sender, e, group_id)
        return
    
def operation_switch_lora(sender, message, group_id):
    if global_var.is_remote_machine:
        return

    if sender != master_id:
        at_user_in_group(sender, sender, "权限不足", group_id)
        return

    new_message = message.replace("#lora", "")
    new_message = new_message.strip()

    response = requests.get(f"{gpu_url}/file=lora_list.txt")

    if response.status_code == 200:
        models = response.content.decode("utf-8").replace('\n','').split('\r')
    else:
        at_user_in_group(sender, sender, "获取模型列表失败", group_id)
        return

    try:
        options = requests.get(f"{gpu_url}/sdapi/v1/options").json()
        at_user_in_group(
            sender, sender, f"当前可用Lora:\n" + "\n".join(models), group_id)

        return
        if new_message == "":
            at_user_in_group(
                sender, sender, f"当前激活Lora:\n{options['sd_model_checkpoint']}\n\n当前可用Lora:\n" + "\n".join(models), group_id)
        else:
            for model_title in models:
                if new_message.lower() in model_title.lower():
                    options['sd_model_checkpoint'] = model_title
                    requests.post(f"{gpu_url}/sdapi/v1/options", json=options)
                    at_user_in_group(sender, sender, f"已切换至模型:\n{model_title}", group_id)
                    return
            at_user_in_group(sender, sender, "未找到匹配的模型", group_id)
    except Exception as e:
        send_err_to_group(sender, e, group_id)
        return

def operation_show_balance(sender, _, group_id):
    if global_var.is_remote_machine:
        return

    response = requests.get("https://api.openai.com/dashboard/billing/credit_grants", headers={
        "Content-Type": 'application/json',
        "Authorization": f"Bearer {api_key}",
    })

    if response.status_code == 200:
        at_user_in_group(sender, sender, response.text, group_id)
    else:
        at_user_in_group(sender, sender, "查询失败:\n" + response.text, group_id)


def operation_set_gpt(sender, message, group_id):
    if sender != master_id and sender not in auth_set_gpt :
        at_user_in_group(sender, sender, "权限不足", group_id)
        return

    new_message = message.replace("#gptset", "")
    new_message = new_message.strip()

    try:
        if new_message == "":
            at_user_in_group(
                sender, sender, f"当前参数:\n{global_var.admin_setGPT}", group_id)
        else:
            new_pair = new_message.split(":")
            if new_pair[-1] != "str":
                new_pair[1] = eval(new_pair)
            global_var.admin_setGPT[new_pair[0]] = new_pair[1]
            at_user_in_group(
                sender, sender, f"修改后的参数:\n{global_var.admin_setGPT}", group_id)
    except Exception as e:
        send_err_to_group(sender, e, group_id)
        return

def operation_chat_prompt_model(sender, message, group_id):
    if global_var.is_remote_machine:
        return

    new_message = message
    for replace_msg in [chat_prompt_model_msg,chat_prompt_model_msg2]:
        new_message = new_message.replace(replace_msg, "")

    new_message = new_message.strip()

    try:
        history_id = get_history_id(group_id, sender)
        if new_message == "":
            at_user_in_group(
                sender, sender, f"当前激活人设:\n{global_var.get_user_cache(history_id).chat_prompt_model}\n\n当前可用人设:\n" + "\n".join(global_var.cur_multi_chatgpt_prompt_base), group_id)
        else:
            for model_title in global_var.cur_multi_chatgpt_prompt_base:
                if new_message.lower() in model_title.lower():
                    global_var.get_user_cache(history_id).chat_prompt_model = model_title
                    at_user_in_group(sender, sender, f"已切换至人设:\n{model_title}", group_id)
                    operation_clear_chat(sender, message, group_id)
                    return
            at_user_in_group(sender, sender, "未找到匹配的人设", group_id)
    except Exception as e:
        send_err_to_group(sender, e, group_id)
        return

def operation_add_chat_prompt_model(sender, message, group_id):
    if global_var.is_remote_machine:
        return

    new_message = message
    for replace_msg in [add_chat_prompt_model_msg,add_chat_prompt_model_msg2,add_chat_prompt_model_msg3,add_chat_prompt_model_msg4,
                        add_chat_prompt_model_msg5,add_chat_prompt_model_msg6,add_chat_prompt_model_msg7,add_chat_prompt_model_msg8]:
        new_message = new_message.replace(replace_msg, "")
    new_message = new_message.strip()
    new_message = new_message.split(" ",1)
    if len(new_message) < 2:
        at_user_in_group(sender, sender, "正确的格式是：[人设名称]空格[人设内容]", group_id)
        return
    model_name = new_message[0]
    new_message = new_message[1].strip()

    try:
        global_var.cur_multi_chatgpt_prompt_base[model_name] = new_message
        at_user_in_group(sender, sender, f"已添加新的人设【{model_name}】", group_id)
    except Exception as e:
        send_err_to_group(sender, e, group_id)
        return

def debug_exec(sender, message, group_id):
    if sender != master_id:
        at_user_in_group(sender, sender, "权限不足", group_id)
        return

    new_message = message.replace("#exec", "")
    new_message = new_message.strip()

    try:
        loc = locals()
        exec(f"cur_debugdata = {new_message}")
        at_user_in_group(sender, sender, f"run successful ! {loc['cur_debugdata']}", group_id)
    except Exception as e:
        send_err_to_group(sender, e, group_id)
        return
    return

both_operations = {
    "#上线": operation_set_online,
    "#下线": operation_set_offline,
    paint_command_msg: operation_gen_image,
    "#d": operation_gen_image,
    delete_command_msg: operation_delete_msg,
    "#拉黑": operation_set_banned,
    "#解除": operation_remove_banned,
    "#vip": operation_add_vip,
    "#unvip": operation_remove_vip,
    "#gpt切换": operation_switch_gpt,
    "#gpt35切换": operation_switch_gpt35,
    "#清理对话": operation_clear_chat,
    "#at切换": operation_switch_at,
    "#语音切换": operation_switch_voice,
    "#音色切换": operation_switch_sound,
    "#朗读": operation_voice,
    "#model": operation_switch_model,
    "#vae": operation_switch_vae,
    '#lora': operation_switch_lora,
    "#余额": operation_show_balance,
    "#gptset": operation_set_gpt,
    chat_prompt_model_msg: operation_chat_prompt_model,
    chat_prompt_model_msg2: operation_chat_prompt_model,
    add_chat_prompt_model_msg: operation_add_chat_prompt_model,
    add_chat_prompt_model_msg2: operation_add_chat_prompt_model,
    add_chat_prompt_model_msg3: operation_add_chat_prompt_model,
    add_chat_prompt_model_msg4: operation_add_chat_prompt_model,
    add_chat_prompt_model_msg5: operation_add_chat_prompt_model,
    add_chat_prompt_model_msg6: operation_add_chat_prompt_model,
    add_chat_prompt_model_msg7: operation_add_chat_prompt_model,
    add_chat_prompt_model_msg8: operation_add_chat_prompt_model,
    "#exec":  debug_exec,
 }

remote_operations = {
    "#帮助": operation_help,
    "#默认": operation_default_config,
    "#黑名单": operation_show_blacklist,
}
