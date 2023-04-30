import streamlit as st
from moviepy.editor import * #pip install moviepy
from moviepy.video.tools.subtitles import SubtitlesClip
import arabic_reshaper # pip install arabic-reshaper
from bidi.algorithm import get_display # pip install python-bidi
import tempfile
import os

st.title('Subtitle App')

# upload audio and srt file with streamlit
video_file = st.file_uploader("Upload Video", type=["mp4", "m4a"])
srt_file = st.file_uploader("Upload Subtitles", type=["srt"])

def generator(txt):
    reshaped_text = arabic_reshaper.reshape(txt)
    bidi_text = get_display(reshaped_text)
    txt_clip = TextClip(bidi_text, font="arial", fontsize=40, color='white', stroke_color="white", stroke_width=2)
    txt_clip = txt_clip.on_color(
        size=(txt_clip.w + 20, txt_clip.h + 20),
        color=(0, 0, 0),
        pos=(-10, 10)
    )
    return txt_clip


if st.button("Add Subtitles"):
    if video_file and srt_file is not None:
        srt_file_path = os.path.abspath(srt_file.name)
        video_file_path = os.path.abspath(video_file.name)

        subs = SubtitlesClip(srt_file_path.name, generator)
        subtitles = subs.set_pos(('center','center'))

        video = VideoFileClip(video_file_path.name)

        # Get the size of the input video
        size = video.size
        result = CompositeVideoClip([video, subtitles], size=size)

        # Create a temporary file to save the result
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file_subtitled:
            # Get the file path string
            temp_file_subtitled_path = temp_file_subtitled.name
            
            # Write the result to the temporary file
            result.write_videofile(temp_file_subtitled_path, codec='mpeg4', audio_codec='aac', bitrate='2000k')
            
            # Display the result
            st.video(temp_file_subtitled_path)
    
    else:
        st.error("Please upload correctly")
    