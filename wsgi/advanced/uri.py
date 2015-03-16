def formatText(text):
    """
    formatText(text) -> uri
    Formats input text to uri friendly format.
    text = input text
    uri = formatted output
    """
    replace_chars = ['-','_','/',':',' ']
    ignore_chars = ['.',',','\'','\"','`']
    
    if not text:
        return ""
    if '(' in text:
        t1 = text.partition('(')
        text = t1[0]+t1.partition(')')[2]
    last_upper = text[0].isupper()
    last_sep = False
    if text[0] not in replace_chars:
        uri = text[0].lower()
    for char in text[1:]:
        if char in replace_chars:
            if not last_sep:
                uri += '-'
            last_sep = True
            last_upper = False
        elif char.isupper():
            if not last_sep and not last_upper:
                uri = uri+'-'+char.lower()
            else:
                uri += char.lower()
            last_sep = False
            last_upper = True
        elif char in ignore_chars:
            pass
        else:
            uri += char
    return uri