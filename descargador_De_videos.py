import streamlit as st
import yt_dlp
import os

# 1. Configuración visual premium (Fondo oscuro por defecto)
st.set_page_config(
    page_title="Descargador de YouTube Premium", 
    page_icon="📥", 
    layout="centered"
)

st.title("📥 Descargador de YouTube Premium")
st.write("---")

# 2. Entrada del Link (Limpia y estilizada)
st.markdown("### **Pega el enlace de YouTube aquí:**")
url = st.text_input(
    label="Entrada de URL",
    label_visibility="collapsed",
    placeholder="https://www.youtube.com/watch?v=..."
)

# 3. Selección del Formato (Equivalente a tus botones segmentados)
st.markdown("#### **Formato de salida:**")
tipo_descarga = st.selectbox(
    label="Selección de formato",
    label_visibility="collapsed",
    options=["Video Completo", "Solo Audio (MP3)"]
)

# 4. Control condicional de opciones (Oculta resolución si elige Audio, igual que tu función original)
ydl_opts = {}
nombre_archivo = "descarga_temporal"
mime_type = "video/mp4"

if tipo_descarga == "Solo Audio (MP3)":
    # Configuración de audio exacta a la tuya
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    nombre_archivo = "audio.mp3"
    mime_type = "audio/mpeg"
else:
    # Selección de la Calidad / Resolución (Solo aparece si es Video)
    st.markdown("#### **Resolución máxima:**")
    calidades = ["144p", "720p", "1080p", "1440p", "2160p"]
    resolucion = st.select_slider(
        label="Selección de resolución",
        label_visibility="collapsed",
        options=calidades,
        value="1080p"  # Tu valor por defecto original
    )
    
    # Asignación de formato según la resolución elegida (Tu lógica exacta)
    if "2160p" in resolucion:
        ydl_opts['format'] = 'bestvideo[height<=2160]+bestaudio/best'
    elif "1440p" in resolucion:
        ydl_opts['format'] = 'bestvideo[height<=1440]+bestaudio/best'
    elif "1080p" in resolucion:
        ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best'
    elif "720p" in resolucion:
        ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best'
    elif "144p" in resolucion:
        ydl_opts['format'] = 'bestvideo[height<=144]+bestaudio/best'
    else:
        ydl_opts['format'] = 'best'
        
    ydl_opts['outtmpl'] = 'video.mp4'
    nombre_archivo = "video.mp4"
    mime_type = "video/mp4"

st.write("")

# 5. Botón de Procesado y descarga (Simula tu botón Rojo vibrante)
if url:
    # Mensaje de estado intermedio
    st.warning("🔄 Procesando descarga... Por favor espera de forma paciente.")
    
    try:
        # Descarga el video temporalmente en el servidor web
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        st.success("✨ ¡Procesado completado con éxito!")
        
        # Este botón VERDE de Streamlit permite enviar el archivo al almacenamiento del teléfono
        with open(nombre_archivo, "rb") as file:
            st.download_button(
                label="📲 Guardar archivo en el teléfono",
                data=file,
                file_name=f"Descarga_YT_{nombre_archivo}",
                mime=mime_type,
                use_container_width=True
            )
            
        # Limpieza automática del servidor para no ocupar espacio
        if os.path.exists(nombre_archivo):
            os.remove(nombre_archivo)
            
    except Exception as e:
        st.error(f"❌ Hubo un error en la descarga:\n{e}")
else:
    st.info("💡 Introduce un enlace válido para activar el descargador.")