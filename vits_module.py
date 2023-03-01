from scipy.io.wavfile import write
from vits.mel_processing import spectrogram_torch
from text import text_to_sequence, _clean_text
import vits.utils as utils
import vits.commons as commons
from vits.models import SynthesizerTrn
import sys
import re
from torch import no_grad, LongTensor
from winsound import PlaySound

idmessage = """ID      Speaker
0       綾地寧々
1       在原七海
2       小茸
3       唐乐吟
"""
speaker_dict = {
    0:"綾地寧々",
    1:"在原七海",
    2:"小茸",
    3:"唐乐吟",
    4:"chisato",
    5:"keqing",
    6:"eula",
}

def get_pth_speaker_id(speakerID):
    if speakerID <= 3:
        return speakerID
    return {
        4:0,
        5:115,
        6:124
    }[speakerID]

def is_multi(speakerID):
    return speakerID in [5,6]

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


    #model = input('Path of a VITS model: ')
    #config = input('Path of a config file: ')
    if language=="ch":
        model = r".\model\CN\model.pth"
        config = r".\model\CN\config.json"
    elif language=="jp":
        model = r".\model\H_excluded.pth"
        config = r".\model\config.json"
    elif language=="multi":
        model = r".\model\Multi\multi.pth"
        config = r".\model\Multi\config.json"

    if speakerID > 3: 
    #   锦木千束
        en_name = speaker_dict[speakerID]
        model = f".\\model\{en_name}\\{en_name}.pth"
        config = r".\model\config804.json"

    hps_ms = utils.get_hparams_from_file(config)
    n_speakers = hps_ms.data.n_speakers if is_multi(speakerID) else 0
    n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0
    speakers = hps_ms.speakers if 'speakers' in hps_ms.keys() else ['0']
    use_f0 = hps_ms.data.use_f0 if 'use_f0' in hps_ms.data.keys() else False
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
            #while True:
            if(1==1):
                #choice = input('TTS or VC? (t/v):')
                choice = 't'
                if choice == 't':
                    #text = input('Text to read: ')
                    text = inputString
                    if text == '[ADVANCED]':
                        #text = input('Raw text:')
                        text = "我不会说"
                        #print('Cleaned text is:')
                        #ex_print(_clean_text(
                        #    text, hps_ms.data.text_cleaners), escape)
                        #continue

                    length_scale, text = get_label_value(
                        text, 'LENGTH', 1.2, 'length scale') #1
                    noise_scale, text = get_label_value(
                        text, 'NOISE', 0.6, 'noise scale') #0.667
                    noise_scale_w, text = get_label_value(
                        text, 'NOISEW', 0.668, 'deviation of noise') #0.8
                    cleaned, text = get_label(text, 'CLEANED')

                    stn_tst = get_text(text, hps_ms, cleaned=cleaned)

                    speaker_id = get_pth_speaker_id(speakerID)
                    #out_path = input('Path to save: ')
                    out_path = "output.wav"

                    with no_grad():
                        x_tst = stn_tst.unsqueeze(0)
                        x_tst_lengths = LongTensor([stn_tst.size(0)])
                        sid = LongTensor([speaker_id])
                        audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale,
                                               noise_scale_w=noise_scale_w, length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()

                write(out_path, hps_ms.data.sampling_rate, audio)
                print('Successfully saved!')
                #ask_if_continue()
