import os
import tkinter as tk
from tkinter import messagebox
import yt_dlp
import threading
import customtkinter as ctk  # Cambiamos a los componentes modernos

# Configuración del estilo visual
ctk.set_appearance_mode("Dark")  # Fondo oscuro premium por defecto
ctk.set_default_color_theme("blue")

def actualizar_opciones(formato_elegido):
    """Oculta o muestra el selector de resolución según el formato."""
    if formato_elegido == "Solo Audio (MP3)":
        res_label.pack_forget()
        selector_resolucion.pack_forget()
    else:
        # Volver a posicionar los elementos en orden si es Video
        res_label.pack(pady=(15, 5))
        selector_resolucion.pack(pady=5)

def descargar_video():
    url = url_entry.get()
    tipo_descarga = selector_tipo.get()
    resolucion = selector_resolucion.get()
    
    if not url.strip():
        messagebox.showwarning("Error", "Por favor, introduce un enlace de YouTube.")
        return

    boton_descargar.configure(state="disabled", text="Descargando...")
    estado_label.configure(text="Descargando... Por favor espera.", text_color="#E67E22")

    def proceso():
        ruta_descargas = os.path.join(os.path.expanduser('~'), 'Downloads')
        ydl_opts = {
            'outtmpl': os.path.join(ruta_descargas, '%(title)s.%(ext)s'),
        }

        if tipo_descarga == "Solo Audio (MP3)":
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
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

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            estado_label.configure(text="¡Descarga completada con éxito!", text_color="#2ECC71")
            messagebox.showinfo("Éxito", "El archivo se ha guardado en tu carpeta de Descargas.")
        except Exception as e:
            estado_label.configure(text="Hubo un error en la descarga.", text_color="#E74C3C")
            messagebox.showerror("Error", f"No se pudo descargar:\n{e}")
        finally:
            boton_descargar.configure(state="normal", text="Descargar Ahora")
            url_entry.delete(0, tk.END)

    threading.Thread(target=proceso).start()


# --- Ventana Principal ---
ventana = ctk.CTk()
ventana.title("Descargador de YouTube Premium")
ventana.geometry("560x420")
ventana.resizable(False, False)

# Entrada del Link (Limpia y estilizada)
instrucciones_label = ctk.CTkLabel(ventana, text="Pega el enlace de YouTube aquí:", font=("Arial", 13, "bold"))
instrucciones_label.pack(pady=(25, 5))

url_entry = ctk.CTkEntry(ventana, width=460, placeholder_text="https://www.youtube.com/watch?v=...", height=35)
url_entry.pack(pady=5)

# Selección del Formato (Botones segmentados en vez de menú desplegable)
tipo_label = ctk.CTkLabel(ventana, text="Formato de salida:", font=("Arial", 12, "bold"), text_color="#A0A0AA")
tipo_label.pack(pady=(20, 5))

selector_tipo = ctk.CTkSegmentedButton(ventana, values=["Video Completo", "Solo Audio (MP3)"], command=actualizar_opciones)
selector_tipo.set("Video Completo")
selector_tipo.pack(pady=5)

# Selección de la Calidad / Resolución (Botones rápidos planos)
res_label = ctk.CTkLabel(ventana, text="Resolución máxima:", font=("Arial", 12, "bold"), text_color="#A0A0AA")
res_label.pack(pady=(15, 5))

calidades = ["144p", "720p", "1080p", "1440p", "2160p"]
selector_resolucion = ctk.CTkSegmentedButton(ventana, values=calidades)
selector_resolucion.set("1080p")  # Por defecto 1080p
selector_resolucion.pack(pady=5)

# Botón Principal de Descarga (Rojo vibrante con bordes redondeados y efecto hover)
boton_descargar = ctk.CTkButton(
    ventana, 
    text="Descargar Ahora", 
    command=descargar_video, 
    fg_color="#FF4757", 
    hover_color="#E83344", 
    font=("Arial", 14, "bold"),
    height=42,
    width=200
)
boton_descargar.pack(pady=30)

# Etiqueta de Estado
estado_label = ctk.CTkLabel(ventana, text="", font=("Arial", 12, "bold"))
estado_label.pack(pady=5)

ventana.mainloop()
