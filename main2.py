import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import face_recognition

known_faces_folder = r'C:\Users\LEGION\Downloads\face\Known faces'
background_image_path = r'C:\Users\LEGION\Downloads\sher-movie-wallpaper-46805.jpg'

def resize_image(image_path, width, height):
    original_image = Image.open(image_path)
    resized_image = original_image.resize((width, height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resized_image)
    return img


def find_matching_face(uploaded_image_path):
    uploaded_image = face_recognition.load_image_file(uploaded_image_path)
    uploaded_face_encoding = face_recognition.face_encodings(uploaded_image)

    if not uploaded_face_encoding:
        return None, None, None

    for root, dirs, files in os.walk(known_faces_folder):
        for file in files:
            known_image_path = os.path.join(root, file)
            known_image = face_recognition.load_image_file(known_image_path)
            known_face_encoding = face_recognition.face_encodings(known_image)[0]

            matches = face_recognition.compare_faces([known_face_encoding], uploaded_face_encoding[0])

            if matches[0]:
                return file.split('.')[0], known_image_path, uploaded_image

    return None, None, uploaded_image

def upload_image(uploaded_image_path, new_name):
    new_image_path = os.path.join(known_faces_folder, f"{new_name}.jpg")
    os.rename(uploaded_image_path, new_image_path)
    print(f"Image uploaded successfully as {new_name}.jpg.")
    return new_image_path

def main():
    root = tk.Tk()
    root.title("Face Recognition App")

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the window size to cover the entire screen
    root.geometry(f"{screen_width}x{screen_height}")

    # Resize the background image to match the window size
    bg_image = resize_image(background_image_path, screen_width, screen_height)

    # Create a Label widget to display the background image
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)

    # Create a Frame to center the widgets at the top
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, pady=20)

    def browse_file():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

    label_path = tk.Label(top_frame, text="Enter the path of the uploaded face image:")
    label_path.pack(side=tk.LEFT, padx=10)

    entry_path = tk.Entry(top_frame, width=50)
    entry_path.pack(side=tk.LEFT)

    button_browse = tk.Button(top_frame, text="Browse", command=browse_file)
    button_browse.pack(side=tk.LEFT, padx=10)

    def process_image():
        uploaded_image_path = entry_path.get()
        matched_name, matched_image_path, uploaded_image = find_matching_face(uploaded_image_path)

        if matched_name:
            result_label.config(text=f"Face found! {matched_name}.")
        else:
            result_label.config(text="Face not found.")
            upload_option = messagebox.askquestion("Upload Image", "Do you want to upload this image to the Known faces folder?")

            if upload_option == 'yes':
                new_name = simpledialog.askstring("Enter Name", "Enter the name of the person:")
                if new_name:
                    uploaded_image_path = upload_image(uploaded_image_path, new_name)
                    result_label.config(text=f"Image uploaded successfully as {new_name}.jpg.")

        # Display the uploaded image
        if uploaded_image:
            img = resize_image(uploaded_image_path, 400, 400)  # Adjust the size as needed
            uploaded_image_label.config(image=img)
            uploaded_image_label.image = img
    button_process = tk.Button(top_frame, text="Process Image", command=process_image)
    button_process.pack(side=tk.LEFT, padx=10)

    # Create a Label to display the uploaded image
    uploaded_image_label = tk.Label(root)
    uploaded_image_label.pack(pady=20)

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
 