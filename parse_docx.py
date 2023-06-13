import docx2txt
import re
import pandas as pd
import streamlit as st

# REGEX patterns
speaker_pattern = re.compile(r'[A-ZÄÖÜ ]+:')
num_pattern = re.compile(r'\d+\/\d+')
timestamp_pattern = re.compile(r'\d+:\d+:\d+:\d+')

def replace_umlauts(text: str) -> str:
    """replace special German umlauts (vowel mutations) from text. 
    ä -> ae, Ä -> Ae...
    ü -> ue, Ü -> Ue...
    ö -> oe, Ö -> Oe...
    ß -> ss
    """
    vowel_char_map = {
        ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe', ord('ß'): 'ss',
        ord('Ä'): 'AE', ord('Ü'): 'UE', ord('Ö'): 'OE'
    }
    return text.translate(vowel_char_map)

def parse_docx(path):
    my_bar = st.progress(0, text="Processing...")
    try:
        text = docx2txt.process(path)
    except:
        return "Error: File could not be read", None
    start_line = text.index('Ende der Inhaltsangabe') + len('Ende der Inhaltsangabe')
    my_text = text[start_line:]
    data = []

    timestamps = re.findall(timestamp_pattern, my_text)
    match = re.split(timestamp_pattern, my_text)
    i = 0

    for m in match:
        # Capitalized alphanumeric string followed by a colon
        line = [j for j in m.splitlines() if not j in ['\xa0', '', '\xa0 ']]

        if not line or line[0].startswith("Take "):
            continue
        
        if i >= len(timestamps):
            break

        start, end = timestamps[i], timestamps[i+1]
        i += 2

        while True:
            if line == []:
                break
            if speaker_pattern.match(line[0]):
                speaker = line[0][:-1]
            elif num_pattern.match(line[0]):
                res = {"speaker": "", "dialogue": "", "take_num": line[0], "start": start, "end": end}
                data.append(res)
                break
            else:
                break
            dialogue = line[1]
            next = 2
            if next >= len(line):
                res = {"speaker": speaker, "dialogue": dialogue, "take_num": take_num, "start": start, "end": end}
                data.append(res)
                break
            if not re.match(speaker_pattern, line[2]) and not re.match(num_pattern, line[2]):
                dialogue += line[2]
                next = 3
            if next >= len(line):
                break
            if re.match(num_pattern, line[next]):
                take_num = line[next]
                line = line[next+1:]
            elif re.match(speaker_pattern, line[next]):
                print("Multiple takes")
                line = line[next:]

            res = {"speaker": speaker, "dialogue": dialogue, "take_num": take_num, "start": start, "end": end}
            data.append(res)
        my_bar.progress(int(i/len(timestamps)*100))
    return "OK", data

def adapt_data(data):
    df = pd.DataFrame(data)
    df["notes"] = ""
    for i, row in df.iterrows():
        if row['take_num'][-1] in ['A','a','Ü','ü']:
            df.at[i,'notes'] = replace_umlauts(row['take_num'][-1])
            df.at[i,'take_num'] = row['take_num'][:-1]

    for i, row in df.iterrows():
        df.at[i,'speaker'] = replace_umlauts(row['speaker']).upper()
        df.at[i,'dialogue'] = replace_umlauts(row['dialogue'])
    
    return df