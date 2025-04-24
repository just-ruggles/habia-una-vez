import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://wallpapers.com/images/hd/black-carbon-fiber-1biekffyzs37csto.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown('<h1 style="color:red;">Friendly Neighbourhood Spider-man App.</h1>', unsafe_allow_html=True)
image = Image.open('fnsm.webp')
st.image(image, width=350)

with st.sidebar:
    st.markdown('<h3 style="color:blue;">Escribe y/o selecciona un texto para ser escuchado.</h3>', unsafe_allow_html=True)

try:
    os.mkdir("temp")
except:
    pass

st.markdown('<h3 style="color:blue;">Una pequeña historia.</h3>', unsafe_allow_html=True)

st.write('Hace mucho tiempo, una pequeña arañita nació. La arañita se sentía muy sola, pero siempre dió lo mejor '  
         ' de sí misma. Años pasaban y la arañita, a pesar de ser muy fuerte, sentía que tenía el peso del mundo ' 
         ' en sus hombros, por lo que se alejó de aquellos que amaba. En medio de su soledad, la arañita conoció '  
         ' a otra como ella, una arañita que necesitaba que le guiaran. Lo que la arañita mayor no sabía, es que ' 
         ' ambos se necesitaban el uno al otro. Ya no era una sola, eran dos pequeñas arañitas explorando la vida. '
         '  '
         ' Yo: Ana. '
        )

st.write('Las interfaces de texto a audio son fundamentales para que la aplicación FNSM funcione perfectamente, '  
         ' pues a veces con todo el ajetreo de luchar contra el crimen y balancearse por las ciudades en telarañas ' 
         ' hace que sea bastante difícil leer la letra en el teléfono. '  
         ' La verdad es que Peter está un poquito muy ciego, y no le da para leer las cosas. '
        )
           
st.markdown('<p style="color:blue;"><strong>¿Quieres escucharlo? copia el texto:</strong></p>', unsafe_allow_html=True)
text = st.text_area("Ingresa el texto a escuchar.")

tld='com'
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English"))
if option_lang=="Español" :
    lg='es'
if option_lang=="English" :
    lg='en'

def text_to_speech(text, tld,lg):
    tts = gTTS(text,lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("convertir a Audio"):
    result, output_text = text_to_speech(text, 'com', lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown('<h3 style="color:blue;">Tú audio:</h3>', unsafe_allow_html=True)
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio File"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

