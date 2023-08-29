import streamlit as st
import cv2
import numpy as np
import tempfile

def extract_stills(video_path, frame_interval):
    frames = []
    timecodes = []
    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_number = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        if frame_number % frame_interval == 0:
            # Convert frame from BGR to RGB color space
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
            timecodes.append(frame_number / fps)

        frame_number += 1

    video_capture.release()
    return frames, timecodes


def display_frames(frames, timecodes):
    for i, frame in enumerate(frames):
        # Display the frame using Streamlit
        st.image(frame, caption=f"Frame {i+1}, Timecode: {timecodes[i]:.2f} seconds")


st.title("Video to Stills Converter")

# Add file upload functionality
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi"])

if uploaded_file is not None:
    # Save the uploaded video to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    video_path = temp_file.name

    # User input for frame grab interval
    #frame_interval = st.slider("Select frame grab interval (in seconds)", 1, 10, 1)

    frame_interval = st.number_input("Select frame grab interval (in seconds)", min_value=None, max_value=None, value=1.0, step=1.0)

    # Convert video to still frames
    frames, timecodes = extract_stills(video_path, int(frame_interval * 30))  # Assuming 30 frames per second

    # Display the number of extracted frames
    st.write("Number of frames extracted:", len(frames))

    # Display the selected frames with timecodes
    display_frames(frames, timecodes)
