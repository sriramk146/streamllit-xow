import cv2
import pytesseract
import re
import streamlit as st
from datetime import timedelta

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


@st.cache_resource
def get_initial_time():
    vid = cv2.VideoCapture("./assets/out.mp4")
    is_success, img = vid.read()
    vid.release()
    if is_success:
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(img, config=custom_config)
        pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
        res = pattern.search(text)
        if res:
            return res.group(0)
    return None


def main():
    initial_time = get_initial_time()
    # print(initial_time)
    if initial_time:
        # st.write(initial_time)
        changing_time = timedelta(hours=0, seconds=0, minutes=0)
        print(changing_time)
        video_file = open("./assets/out.mp4", 'rb')
        video_bytes = video_file.read()
        placeholder = st.empty()
        placeholder.video(video_bytes, start_time=changing_time)
        start_time = st.text_input("Goto", initial_time)
        if start_time != initial_time:
            try:
                start_time = re.search(r'\d{2}:\d{2}:\d{2}', start_time).group(0)
                initial_hours, initial_minutes, initial_seconds = map(int, initial_time.split(":"))
                hours, minutes, seconds = map(int, start_time.split(":"))
                changing_time = timedelta(hours=hours - initial_hours, minutes=minutes - initial_minutes, seconds=seconds - initial_seconds)
                placeholder.video(video_bytes, start_time=changing_time, autoplay=True)
            except:
                st.write("Invalid time format. Please enter time in HH:MM:SS format.")

    else:
        st.write("Time not found in the first frame of the video.")


if __name__ == "__main__":
    st.set_page_config(page_title="Video Player", page_icon="📹", layout="centered")
    main()
