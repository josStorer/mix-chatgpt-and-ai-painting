import json
import base64
import global_var
from pydub import AudioSegment
from vits_module import generateSound
import re
# 音频文件路径
path_in = f"{global_var.cwd_path}\\output.wav"
path_out = f"{global_var.cwd_path}\\output.mp3"
word_before_voice = "我想说的话已经通过语音传达了喵~希望你能听见"

def word_cleaner(message):
    message = re.sub(global_var.reg_dirty,'**',message)
    return message

def send_message_to_group(message_source, message, group_id, bCleaned = False):
    print(f"[Res]{message}[Res]")
    global_var.ws.send(json.dumps({
        "action": "send_group_msg",
        "params": {
            "group_id": str(group_id),
            "message": word_cleaner(message) if not bCleaned else message
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

def send_record_to_group(message_source, message, group_id, speakerID = 3):
    message = re.sub(r'\[CQ:.*\]', '', message).replace('\n','')
    if speakerID != 7:
        message = f"[ZH]{message}[ZH]"
    print(f"{message}")
    generateSound(f"{message}","ch",speakerID)
    # 读取音频文件，设置采样率<default=44100>
    song = AudioSegment.from_wav(path_in).set_frame_rate(22050)
    # 按32k的bitrate导出文件到指定路径,这里是直接覆盖原文件
    fh = song.export(path_out, format='mp3', bitrate='32k')
    # sound = miraicle.Voice(base64=path_out)
    global_var.ws.send(json.dumps({
        "action": "send_group_msg",
        "params": {
            "group_id": str(group_id),
            "message": f"[CQ:record,file=base64://{base64.b64encode(fh.read())}]".replace('b\'','').replace('\'','')
        },
        "echo": {
            "message_source": message_source
        }
    }))
    send_message_to_group(message_source, f"[CQ:at,qq={message_source}]\n{message}", group_id)

def send_record_to_group_jp(message_source, message, group_id, speakerID = 3):
    message = re.sub(r'\[CQ:.*\]', '', message).replace('\n','')
    print(f"{message}")
    generateSound(f"{message}","jp",speakerID)
    # 读取音频文件，设置采样率<default=44100>
    song = AudioSegment.from_wav(path_in).set_frame_rate(22050)
    # 按32k的bitrate导出文件到指定路径,这里是直接覆盖原文件
    fh = song.export(path_out, format='mp3', bitrate='32k')
    # sound = miraicle.Voice(base64=path_out)
    global_var.ws.send(json.dumps({
        "action": "send_group_msg",
        "params": {
            "group_id": str(group_id),
            "message": f"[CQ:record,file=base64://{base64.b64encode(fh.read())}]".replace('b\'','').replace('\'','')
        },
        "echo": {
            "message_source": message_source
        }
    }))
    send_message_to_group(message_source, f"[CQ:at,qq={message_source}]\n{message}", group_id)
