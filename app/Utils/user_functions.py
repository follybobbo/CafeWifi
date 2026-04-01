
#check if file name has a . and if extension of picture is in allowed
def is_photo_file_allowed(photo_name: str, allowed_extensions: list):
    photo_extension = photo_name.rsplit(".", 1)[1].lower()
    return  "." in photo_name and photo_extension in allowed_extensions