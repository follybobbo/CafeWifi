from flask_login import current_user
from flask import current_app, flash, jsonify, redirect, url_for
import os

#takes folder where images are stored as an argument, loops through the list of files in that folder and delete the files.
def delete_existing_pictures_in_folder(folder):
    list_of_files = os.listdir(folder)
    for file in list_of_files:
        file_path = os.path.join(folder, file)

        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            pass


# def save_display_picture(file, secure_file_path):
#     try:
#         file.save(secure_file_path)
#     except Exception as e:
#         flash(f"An Error Occurred: {e}", "info")
#         return jsonify({"message": "Failed to save picture"}), 400
#     else:
#         # save picture path to db.
#         print("saved to db")
#         flash("display picture uploaded successfully", "success")
#         # update_user_display_picture(current_user.id, path)
#         return redirect(url_for("protected.dashboard"))
