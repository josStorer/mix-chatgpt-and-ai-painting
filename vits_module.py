from vits_const import *
from scipy.io.wavfile import write
from vits.mel_processing import spectrogram_torch
from text import text_to_sequence, text_to_sequence_paimon
import vits.utils as utils
import vits.commons as commons
from vits.models import SynthesizerTrn
import sys
import re
from torch import no_grad, LongTensor
from winsound import PlaySound
from vits.symbols import symbols as symbols_for_paimon
import global_var

speaker_dict = {
    0:"綾地寧々",
    1:"在原七海",
    2:"小茸",
    3:"唐乐吟",
    4:"chisato",
    5:"keqing",
    6:"eula",
    Paimon_Test_Index:"paimon",
}

def get_pth_speaker_id(speakerID):
    if speakerID <= 3:
        return speakerID
    return {
        4:0,
        5:115,
        6:124,
        Paimon_Test_Index:0
    }[speakerID]

def is_multi(speakerID):
    return speakerID in [0,1,2,3,5,6]

def get_lnnw(speakerID):
    if speakerID <= 3 or speakerID == Paimon_Test_Index:
        return 1, 0.667, 0.8
    return 1.2, 0.6, 0.668

def ex_print(text, escape=False):
    if escape:
        print(text.encode('unicode_escape').decode())
    else:
        print(text)

def get_text(text, hps, cleaned=False):
    if cleaned:
        text_norm = text_to_sequence(text, hps.symbols, [])
    else:
        text_norm = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm

def get_text_paimon(text, hps):
    text_norm = text_to_sequence_paimon(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm

def print_speakers(speakers, escape=False):
    if len(speakers) > 100:
        return
    print('ID\tSpeaker')
    for id, name in enumerate(speakers):
        ex_print(str(id) + '\t' + name, escape)


def get_label_value(text, label, default, warning_name='value'):
    value = re.search(rf'\[{label}=(.+?)\]', text)
    if value:
        try:
            text = re.sub(rf'\[{label}=(.+?)\]', '', text, 1)
            value = float(value.group(1))
        except:
            print(f'Invalid {warning_name}!')
            sys.exit(1)
    else:
        value = default
    return value, text


def get_label(text, label):
    if f'[{label}]' in text:
        return True, text.replace(f'[{label}]', '')
    else:
        return False, text


def generateSound(inputString,language,speakerID = 3):
    if '--escape' in sys.argv:
        escape = True
    else:
        escape = False

    if language=="ch":
        model = f"{global_var.cwd_path}\\model\\CN\\model.pth"
        config = f"{global_var.cwd_path}\\model\\CN\\config.json"
    elif language=="jp":
        model = f"{global_var.cwd_path}\\model\\H_excluded.pth"
        config = f"{global_var.cwd_path}\\model\\config.json"
    elif language=="multi":
        model = f"{global_var.cwd_path}\\model\\Multi\\multi.pth"
        config = f"{global_var.cwd_path}\\model\\Multi\\config.json"

    if speakerID > 3: 
    #   锦木千束
        en_name = speaker_dict[speakerID]
        model = f"{global_var.cwd_path}\\model\\{en_name}\\{en_name}.pth"
        config = f"{global_var.cwd_path}\\model\\config804.json"

        if speakerID == Paimon_Test_Index:
            config = f"{global_var.cwd_path}\\model\\{en_name}\\config_{en_name}.json"
            hps_ms = utils.get_hparams_from_file(config)
            net_g = SynthesizerTrn(
                len(symbols_for_paimon),
                hps_ms.data.filter_length // 2 + 1,
                hps_ms.train.segment_size // hps_ms.data.hop_length,
                **hps_ms.model)
            _ = net_g.eval()

            _ = utils.load_checkpoint(model, net_g)
            import soundfile as sf
            text = inputString # "现在是派蒙与您对话" #@param {type: 'string'}
            length_scale = 1 #@param {type:"slider", min:0.1, max:3, step:0.05}
            filename = 'output' #@param {type: "string"}
            audio_path = f'{global_var.cwd_path}\\{filename}.wav'
            stn_tst = get_text_paimon(text, hps_ms)
            with no_grad():
                x_tst = stn_tst.unsqueeze(0)
                x_tst_lengths = LongTensor([stn_tst.size(0)])
                audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=length_scale)[0][0,0].data.cpu().float().numpy()

            sf.write(audio_path,audio,samplerate=hps_ms.data.sampling_rate)
            print('Successfully saved!')
            return

    hps_ms = utils.get_hparams_from_file(config)
    n_speakers = hps_ms.data.n_speakers if is_multi(speakerID) else 0
    # @note:留着这段，以后再做通用处理吧，累了
    # if speakerID == Paimon_Test_Index:
    #     hps_ms.symbols = symbols_for_paimon
    n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0
    emotion_embedding = hps_ms.data.emotion_embedding if 'emotion_embedding' in hps_ms.data.keys() else False

    net_g_ms = SynthesizerTrn(
        n_symbols,
        hps_ms.data.filter_length // 2 + 1,
        hps_ms.train.segment_size // hps_ms.data.hop_length,
        n_speakers=n_speakers,
        emotion_embedding=emotion_embedding,
        **hps_ms.model)
    _ = net_g_ms.eval()
    utils.load_checkpoint(model, net_g_ms)

    if n_symbols != 0:
        if not emotion_embedding:
            text = inputString
            if text == '[ADVANCED]':
                text = "我不会说"

            length_scale, noise_scale, noise_scale_w = get_lnnw(speakerID)

            cleaned, text = get_label(text, 'CLEANED')

            stn_tst = get_text(text, hps_ms, cleaned=cleaned)

            speaker_id = get_pth_speaker_id(speakerID)

            out_path = f"{global_var.cwd_path}\\output.wav"

            with no_grad():
                x_tst = stn_tst.unsqueeze(0)
                x_tst_lengths = LongTensor([stn_tst.size(0)])
                sid = LongTensor([speaker_id])
                audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale,
                                        noise_scale_w=noise_scale_w, length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()

        write(out_path, hps_ms.data.sampling_rate, audio)
        print('Successfully saved!')
