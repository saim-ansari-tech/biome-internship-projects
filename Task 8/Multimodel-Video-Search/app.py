from flask import Flask, render_template

app = Flask(__name__)




from flask import Flask,request,jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER="uploads"

os.makedirs(UPLOAD_FOLDER,exist_ok=True)

app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER


@app.route("/upload",methods=["POST"])
def upload():

    file=request.files["video"]

    filename=secure_filename(file.filename)

    save_path=os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(save_path)

    # AI Pipeline
    # result = process_video(save_path)

    return jsonify({
        "success":True
    })

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/processing")
def processing():
    return render_template("processing.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/search")
def search():
    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)