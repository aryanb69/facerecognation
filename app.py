from flask import Flask, render_template, request, redirect, url_for
import os
import face_recognition

app = Flask(__name__)

known_faces_folder = r'C:\Users\LEGION\Downloads\face\Known faces'

def find_matching_face(uploaded_image_path):
    uploaded_image = face_recognition.load_image_file(uploaded_image_path)
    uploaded_face_encoding = face_recognition.face_encodings(uploaded_image)

    if not uploaded_face_encoding:
        return None, None

    for root, dirs, files in os.walk(known_faces_folder):
        for file in files:
            known_image_path = os.path.join(root, file)
            known_image = face_recognition.load_image_file(known_image_path)
            known_face_encoding = face_recognition.face_encodings(known_image)[0]

            matches = face_recognition.compare_faces([known_face_encoding], uploaded_face_encoding[0])

            if matches[0]:
                return file.split('.')[0], known_image_path

    return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle the uploaded image
        uploaded_image = request.files['uploaded_image']
        uploaded_image_path = os.path.join("uploads", uploaded_image.filename)
        uploaded_image.save(uploaded_image_path)

        # Find matching face
        matched_name, matched_image_path = find_matching_face(uploaded_image_path)

        if matched_name:
            return render_template('result.html', result=f"Face found! {matched_name}.")
        else:
            return render_template('confirm_upload.html', uploaded_image_path=uploaded_image_path)

    return render_template('index.html')

@app.route('/confirm_upload', methods=['POST'])
@app.route('/confirm_upload', methods=['POST'])
def confirm_upload():
    upload_option = request.form.get('upload_option')
    uploaded_image_path = request.form.get('uploaded_image_path')

    if upload_option.lower() == 'yes':
        return render_template('enter_name.html', uploaded_image_path=uploaded_image_path)
    else:
        os.remove(uploaded_image_path)
        return render_template('result.html', result="Image not uploaded.")

@app.route('/enter_name', methods=['POST'])
def enter_name():
    new_name = request.form.get('new_name')
    uploaded_image_path = request.form.get('uploaded_image_path')

    print(f"Debug: new_name = {new_name}")
    print(f"Debug: uploaded_image_path = {uploaded_image_path}")

    new_image_path = os.path.join(known_faces_folder, f"{new_name}.jpg")
    print(f"Debug: new_image_path = {new_image_path}")

    os.rename(uploaded_image_path, new_image_path)

    return render_template('result.html', result=f"Image uploaded successfully as {new_name}.jpg.")
@app.route('/reset', methods=['GET'])
def reset():
    return redirect(url_for('index'))


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
