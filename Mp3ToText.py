from gtts import gTTS
import playsound


def mp3_convert(text_input):
    my_text = text_input
    language = 'sk'
    my_obj = gTTS(text=my_text, lang=language, slow=False)
    my_obj.save("welcome.mp3")

    # Playing the converted file
    playsound.playsound("welcome.mp3")
