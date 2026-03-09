
def slugify(text):
    stringed_text = str(text)
    text = stringed_text.replace(" ", "-")

    return text

def de_slugify(slugified_text):
    normalised_text = str(slugified_text).replace("-", " ")

    return normalised_text


