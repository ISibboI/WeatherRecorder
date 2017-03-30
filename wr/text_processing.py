def cut(text, marker):
    index = text.index(marker)
    return text[:index], text[index + len(marker):]


def retain_after(text, marker):
    return cut(text, marker)[1]


def retain_before(text, marker):
    return cut(text, marker)[0]
