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
                send_err_to_group(sender, str(e), group_id)
    else:
        try:
            res = new_message.replace(";", ".").split('.', 3)
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
                send_err_to_group(sender, str(e), group_id)


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
    "#gpt切换": operation_switch_gpt
}

remote_operations = {
    "#帮助": operation_help,
    "#默认": operation_default_config,
    "#黑名单": operation_show_blacklist,
}
