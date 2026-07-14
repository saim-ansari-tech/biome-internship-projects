from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)

from utils.file_handler import save_uploaded_file
from utils.embedding import generate_embedding
from utils.storage import (
    user_exists,
    save_embeddings,
    load_embedding
)
from utils.similarity import (
    calculate_similarity,
    is_authenticated
)
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        audio_file = request.files.get("audiofile")

        if not username:
            flash("Please enter a username.", "error")
            return redirect(url_for("register"))

        if not audio_file or audio_file.filename == "":
            flash("Please upload a voice sample.", "error")
            return redirect(url_for("register"))

        if user_exists(username):
            flash("Username already exists.", "error")
            return redirect(url_for("register"))

        try:
            file_path = save_uploaded_file(audio_file)

            embedding = generate_embedding(file_path)

            save_embeddings(username, embedding)

            flash("Registration completed successfully!", "success")

        except Exception as e:
            flash(f"Registration failed: {str(e)}", "error")

        return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/authenticate", methods=["GET", "POST"])
def authenticate():

    if request.method == "POST":

        username = request.form.get("username")
        audio_file = request.files.get("audiofile")

        if not username:
            flash("Please enter your username.", "error")
            return redirect(url_for("authenticate"))

        if not audio_file or audio_file.filename == "":
            flash("Please upload a voice sample.", "error")
            return redirect(url_for("authenticate"))

        if not user_exists(username):
            flash("User not found. Please register first.", "error")
            return redirect(url_for("authenticate"))

        try:
            file_path = save_uploaded_file(audio_file)

            new_embedding = generate_embedding(file_path)

            registered_embedding = load_embedding(username)

            similarity_score = calculate_similarity(
                registered_embedding,
                new_embedding
            )

            print(f"Similarity Score: {similarity_score:.4f}")

            if is_authenticated(similarity_score):
                flash(
                    f"Authentication Successful!"
                    f"Similarity Score: {similarity_score:.4f}",
                    "success"
                )
            else:
                flash(
                    f"Authentication Failed! Similarity Score:"
                    f"{similarity_score:.4f}",
                    "error"
                )

        except Exception as e:
            flash(f"Authentication Error: {str(e)}", "error")

        return redirect(url_for("authenticate"))

    return render_template("authenticate.html")


if __name__ == "__main__":
    app.run(debug=True)
