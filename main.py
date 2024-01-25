import os
import streamlit as st
import face_recognition
import numpy as np
from PIL import Image

known_faces_folder = r'C:\Users\LEGION\Downloads\face\Known faces'

def find_matching_face(uploaded_image):
    # Convert the UploadedFile to a numpy array
    uploaded_image_np = np.array(Image.open(uploaded_image))

    uploaded_face_encoding = face_recognition.face_encodings(uploaded_image_np)

    if not uploaded_face_encoding:
        return None, None

    for root, dirs, files in os.walk(known_faces_folder):
        for file in files:
            known_image_path = os.path.join(root, file)
            try:
                known_image = face_recognition.load_image_file(known_image_path)
            except face_recognition.ImageFormatError:
                continue  # Skip unsupported image formats
            known_face_encoding = face_recognition.face_encodings(known_image)[0]

            matches = face_recognition.compare_faces([known_face_encoding], uploaded_face_encoding[0])

            if matches[0]:
                return file.split('.')[0], known_image_path

    return None, None

def main():
    st.title("Face Recognition App ")

    uploaded_image = st.file_uploader("Upload Face Image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        matched_name, matched_image_path = find_matching_face(uploaded_image)

        if matched_name:
            st.success(f"Face found! {matched_name}.")
        else:
            st.warning("Face not found.")
            upload_option = st.radio("Do you want to upload this image to the Known faces folder?", ('Yes', 'No'))

            if upload_option == 'Yes':
                new_name = st.text_input("Enter the name of the person:")
                if new_name:
                    new_image_path = os.path.join(known_faces_folder, f"{new_name}.jpg")
                    uploaded_image_np = np.array(Image.open(uploaded_image))
                    Image.fromarray(uploaded_image_np).save(new_image_path)
                    st.success(f"Image uploaded successfully as {new_name}.jpg.")
                else:
                    st.warning("Please enter a name to upload the image.")
            else:
                st.info("Image not uploaded.")

if __name__ == "__main__":
    main()
