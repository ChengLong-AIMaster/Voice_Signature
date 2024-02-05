from flask import Flask, render_template, request
import os
import shutil
from speechbrain.pretrained import SpeakerRecognition

app = Flask(__name__)

current_working_directory = os.getcwd()

temp_folder = './temp'
cash_folder = './audio_cache'

def empty_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
        

@app.route("/signin", methods = ["GET", "POST"])
def signin():
    if request.method == 'POST':
        try:
            file = request.files['file']
            
            if 'file' not in request.files:
                return 'No file part'
            
            if file.filename == '':
                return 'No selected file'
            
            if file:
                file.save(current_working_directory + "/temp/" + file.filename)
                verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")
                score, prediction = verification.verify_files("./user/origin.wav", "./temp/" + file.filename)
        
                empty_folder(temp_folder)
                empty_folder(cash_folder)

                if prediction == True:
                    return "same person"
                else:
                    return "diff person"
                    
        except Exception as e:
            return 'An error occured during file upload'
    return "diff person"

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == 'POST':
        try:
            file = request.files['file']
            
            if 'file' not in request.files:
                return 'No file part'
            
            if file.filename == '':
                return 'No selected file'
            
            if file:
                file.save(current_working_directory + "/user/" + "origin.wav")
                return 'success'
                    
        except Exception as e:
            return 'An error occured during file upload'
    return 'siginup error'
    

if __name__ == "__main__":
    app.run()
    
    
    
    
    
    
    
    
    