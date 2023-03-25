import re
import jieba, cn2an
from pypinyin import lazy_pinyin, BOPOMOFO

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

def japanese_cleaners(text):
    from text.japanese import japanese_to_romaji_with_accent
    text = japanese_to_romaji_with_accent(text)
    text = re.sub(r'([A-Za-z])$', r'\1.', text)
    return text


def japanese_cleaners2(text):
    return japanese_cleaners(text).replace('ts', 'ʦ').replace('...', '…')


def korean_cleaners(text):
    '''Pipeline for Korean text'''
    from text.korean import latin_to_hangul, number_to_hangul, divide_hangul
    text = latin_to_hangul(text)
    text = number_to_hangul(text)
    text = divide_hangul(text)
    text = re.sub(r'([\u3131-\u3163])$', r'\1.', text)
    return text


def chinese_cleaners(text):
    '''Pipeline for Chinese text'''
    from text.mandarin import number_to_chinese, chinese_to_bopomofo, latin_to_bopomofo
    text = number_to_chinese(text)
    text = chinese_to_bopomofo(text)
    text = latin_to_bopomofo(text)
    text = re.sub(r'([ˉˊˇˋ˙])$', r'\1。', text)
    return text


def zh_ja_mixture_cleaners(text):
    from text.japanese import japanese_to_romaji_with_accent
    from text.mandarin import number_to_chinese,chinese_to_bopomofo,latin_to_bopomofo,bopomofo_to_romaji
    chinese_texts=re.findall(r'\[ZH\].*?\[ZH\]',text)
    japanese_texts=re.findall(r'\[JA\].*?\[JA\]',text)
    for chinese_text in chinese_texts:
        cleaned_text = number_to_chinese(chinese_text[4:-4])
        cleaned_text = chinese_to_bopomofo(cleaned_text)
        cleaned_text = latin_to_bopomofo(cleaned_text)
        cleaned_text = bopomofo_to_romaji(cleaned_text)
        cleaned_text = re.sub('i[aoe]',lambda x:'y'+x.group(0)[1:],cleaned_text)
        cleaned_text = re.sub('u[aoəe]',lambda x:'w'+x.group(0)[1:],cleaned_text)
        cleaned_text = re.sub('([ʦsɹ]`[⁼ʰ]?)([→↓↑]+)',lambda x:x.group(1)+'ɹ`'+x.group(2),cleaned_text).replace('ɻ','ɹ`')
        cleaned_text = re.sub('([ʦs][⁼ʰ]?)([→↓↑]+)',lambda x:x.group(1)+'ɹ'+x.group(2),cleaned_text)
        text = text.replace(chinese_text,cleaned_text+' ',1)
    for japanese_text in japanese_texts:
        cleaned_text=japanese_to_romaji_with_accent(japanese_text[4:-4]).replace('ts','ʦ').replace('u','ɯ').replace('...','…')
        text = text.replace(japanese_text,cleaned_text+' ',1)
    text = text[:-1]
    if re.match('[A-Za-zɯɹəɥ→↓↑]',text[-1]):
        text += '.'
    return text


def sanskrit_cleaners(text):
    text = text.replace('॥', '।').replace('ॐ', 'ओम्')
    text = re.sub(r'([^।])$', r'\1।', text)
    return text


def cjks_cleaners(text):
    from text.mandarin import chinese_to_lazy_ipa
    from text.japanese import japanese_to_ipa
    from text.korean import korean_to_lazy_ipa
    from text.sanskrit import devanagari_to_ipa
    from text.english import english_to_lazy_ipa
    text = re.sub(r'\[ZH\](.*?)\[ZH\]',
                  lambda x: chinese_to_lazy_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[JA\](.*?)\[JA\]',
                  lambda x: japanese_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[KO\](.*?)\[KO\]',
                  lambda x: korean_to_lazy_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[SA\](.*?)\[SA\]',
                  lambda x: devanagari_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[EN\](.*?)\[EN\]',
                  lambda x: english_to_lazy_ipa(x.group(1))+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text


def cjke_cleaners(text):
    from text.mandarin import chinese_to_lazy_ipa
    from text.japanese import japanese_to_ipa
    from text.korean import korean_to_ipa
    from text.english import english_to_ipa2
    text = re.sub(r'\[ZH\](.*?)\[ZH\]', lambda x: chinese_to_lazy_ipa(x.group(1)).replace(
        'ʧ', 'tʃ').replace('ʦ', 'ts').replace('ɥan', 'ɥæn')+' ', text)
    text = re.sub(r'\[JA\](.*?)\[JA\]', lambda x: japanese_to_ipa(x.group(1)).replace('ʧ', 'tʃ').replace(
        'ʦ', 'ts').replace('ɥan', 'ɥæn').replace('ʥ', 'dz')+' ', text)
    text = re.sub(r'\[KO\](.*?)\[KO\]',
                  lambda x: korean_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[EN\](.*?)\[EN\]', lambda x: english_to_ipa2(x.group(1)).replace('ɑ', 'a').replace(
        'ɔ', 'o').replace('ɛ', 'e').replace('ɪ', 'i').replace('ʊ', 'u')+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text


def cjke_cleaners2(text):
    from text.mandarin import chinese_to_ipa
    from text.japanese import japanese_to_ipa2
    from text.korean import korean_to_ipa
    from text.english import english_to_ipa2
    text = re.sub(r'\[ZH\](.*?)\[ZH\]',
                  lambda x: chinese_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[JA\](.*?)\[JA\]',
                  lambda x: japanese_to_ipa2(x.group(1))+' ', text)
    text = re.sub(r'\[KO\](.*?)\[KO\]',
                  lambda x: korean_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[EN\](.*?)\[EN\]',
                  lambda x: english_to_ipa2(x.group(1))+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text


def thai_cleaners(text):
    from text.thai import num_to_thai, latin_to_thai
    text = num_to_thai(text)
    text = latin_to_thai(text)
    return text


def shanghainese_cleaners(text):
    from text.shanghainese import shanghainese_to_ipa
    text = shanghainese_to_ipa(text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text


def chinese_dialect_cleaners(text):
    from text.mandarin import chinese_to_ipa2
    from text.japanese import japanese_to_ipa3
    from text.shanghainese import shanghainese_to_ipa
    from text.cantonese import cantonese_to_ipa
    from text.english import english_to_lazy_ipa2
    from text.ngu_dialect import ngu_dialect_to_ipa
    text = re.sub(r'\[ZH\](.*?)\[ZH\]',
                  lambda x: chinese_to_ipa2(x.group(1))+' ', text)
    text = re.sub(r'\[JA\](.*?)\[JA\]',
                  lambda x: japanese_to_ipa3(x.group(1)).replace('Q', 'ʔ')+' ', text)
    text = re.sub(r'\[SH\](.*?)\[SH\]', lambda x: shanghainese_to_ipa(x.group(1)).replace('1', '˥˧').replace('5',
                  '˧˧˦').replace('6', '˩˩˧').replace('7', '˥').replace('8', '˩˨').replace('ᴀ', 'ɐ').replace('ᴇ', 'e')+' ', text)
    text = re.sub(r'\[GD\](.*?)\[GD\]',
                  lambda x: cantonese_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[EN\](.*?)\[EN\]',
                  lambda x: english_to_lazy_ipa2(x.group(1))+' ', text)
    text = re.sub(r'\[([A-Z]{2})\](.*?)\[\1\]', lambda x: ngu_dialect_to_ipa(x.group(2), x.group(
        1)).replace('ʣ', 'dz').replace('ʥ', 'dʑ').replace('ʦ', 'ts').replace('ʨ', 'tɕ')+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text

def chinese_cleaners1(text):
    from pypinyin import Style, pinyin

    phones = [phone[0] for phone in pinyin(text, style=Style.TONE3)]
    return ' '.join(phones)
