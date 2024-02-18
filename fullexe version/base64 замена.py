import base64

def file_to_base64(file_path):
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode("utf-8")
    return encoded_string

# Замените "logo.png" на путь к вашему файлу logo.png и так далее для других файлов
logo_base64 = file_to_base64("logo.png")
tree_base64 = file_to_base64("tree.png")
start_sound_base64 = file_to_base64("start_sound.wav")
end_sound_base64 = file_to_base64("end_sound.wav")
close_button_base64 = file_to_base64("close_button.png")
question_button_base64 = file_to_base64("question_button.png")

print("START_SOUND_BASE64 =", repr(start_sound_base64))
