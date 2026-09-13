import streamlit as st
import os
import yt_dlp

# Создаем папки для хранения результатов, если их еще нет
os.makedirs('downloads/videos/', exist_ok=True)
os.makedirs('downloads/audio/', exist_ok=True)

st.set_page_config(page_title="Автономный архиватор контента", layout="centered")

# Заголовок
st.title("Автономный архиватор контента")

# Поле для ввода ссылки
video_url = st.text_input("Введите ссылку на видео (YouTube или Rutube):")

# Выбор действия: скачать видео или только аудио
download_option = st.selectbox(
    "Что скачать?",
    ("Скачать только Аудио (MP3)", "Скачать Видео (Максимальное качество)")
)

# Кнопка запуска
if st.button("Запустить скачивание"):
    if not video_url:
        st.error("Пожалуйста, введите ссылку")
    else:
        try:
            with st.spinner('Обрабатываю...'):
                # Настройки yt_dlp в зависимости от выбранной опции
                if download_option == "Скачать только Аудио (MP3)":
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': 'downloads/audio/%(title)s.%(ext)s',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'quiet': True,
                        'nocheckcertificate': True,
                        'no_warnings': True,
                        # Для Rutube добавьте User-Agent и Referer
                        'write_info_json': False,  # отключение extra info для чистоты
                        'prefer_insecure': True,
                        'http_headers': {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                            'Referer': 'https://rutube.ru/'
                        },
                        'Ignoreerrors': True,
                    }
                else:
                    # Скачать видео в лучшем качестве
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': 'downloads/videos/%(title)s.%(ext)s',
                        'quiet': True,
                        'nocheckcertificate': True,
                        'no_warnings': True,
                        'merge_output_format': 'mp4',
                        'http_headers': {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                            'Referer': 'https://rutube.ru/'
                        },
                        'Ignoreerrors': True,
                    }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])

            st.success("Успешно скачано!")
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
