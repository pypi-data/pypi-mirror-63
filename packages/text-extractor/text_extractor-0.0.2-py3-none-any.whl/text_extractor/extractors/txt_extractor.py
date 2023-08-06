def txt_extract(filepath, **kwargs):
    with open(filepath, "r", encoding = "utf-8") as f:
        text = f.read()
    return text

extract = txt_extract    