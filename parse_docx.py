from docx.api import Document
import pandas as pd

def replace_umlauts(text: str) -> str:
    """replace special German umlauts (vowel mutations) from text. 
    ä -> ae, Ä -> Ae...
    ü -> ue, Ü -> Ue...
    ö -> oe, Ö -> Oe...
    ß -> ss
    """
    vowel_char_map = {
        ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe', ord('ß'): 'ss',
        ord('Ä'): 'Ae', ord('Ü'): 'Ue', ord('Ö'): 'Oe'
    }
    return text.translate(vowel_char_map)

def docx_to_csv(path):
    # Load the first table from your document. In your example file,
    # there is only one table, so I just grab the first one.
    try:
        document = Document(path)
    except:
        return "Not a valid docx file", pd.DataFrame()
    try:
        table = document.tables[0]
    except:
        return "No table found", pd.DataFrame()
    # Data will be a list of rows represented as dictionaries
    # containing each row's data.
    data = []

    keys = None
    for i in range(0, len(table.rows), 3):
        dialogue = table.cell(i, 0).text
        start_take = table.cell(i, 1).text
        take_num = table.cell(i+1, 1).text
        end_take = table.cell(i+2, 1).text
        data.append({'dialogue': dialogue, 'start_take': start_take, 'take_num': take_num, 'end_take': end_take})

    takes = []
    for take in data:
        for line in take["dialogue"].split('\n'):
            speaker = line.split(':')[0]
            text = line.split(':')[1]
            start_take = take["start_take"]
            take_num = take["take_num"]
            end_take = take["end_take"]
            takes.append({'speaker': str.upper(replace_umlauts(speaker)), 'text': replace_umlauts(text), 'start_take': start_take, 'take_num': take_num, 'end_take': end_take})

    df = pd.DataFrame(takes)
    return "OK", df