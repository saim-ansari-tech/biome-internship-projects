from pathlib import Path
from flask import (
    Flask,
    jsonify,
    render_template,
    request
)

from werkzeug.utils import secure_filename

from src.document_loader import (
    text_loader,
    pdf_loader,
    doc_loader,
)

from src.document_splitter import (
    text_splitter
)

from src.vector_store import (
    create_vector_store,
    get_vector_store
)

from src.sementic_search import (
    semantic_search
)

from src.llm_generator import (
    generate_answer
)


app = Flask(
    __name__
)


UPLOAD_FOLDER = Path(
    "data/documents"
)

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

ALLOWED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx"
}

document_uploaded = False


@app.route("/")
def index():

    return render_template(
        "index.html"
    )


def allowed_file(
    filename
):

    file_path = Path(
        filename
    )

    return (
        file_path.suffix.lower()
        in ALLOWED_EXTENSIONS
    )


def load_document(
    file_path
):

    file_type = (
        file_path.suffix.lower()
    )

    if file_type == ".txt":

        return text_loader(
            file_path
        )

    elif file_type == ".pdf":

        return pdf_loader(
            file_path
        )

    elif file_type == ".docx":

        return doc_loader(
            file_path
        )

    else:

        raise ValueError(
            "Unsupported file type."
        )


@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    global document_uploaded

    try:

        if "file" not in request.files:

            return jsonify({

                "error":
                    "No file uploaded."

            }), 400

        file = request.files[
            "file"
        ]

        if file.filename == "":

            return jsonify({

                "error":
                    "No file selected."

            }), 400

        if not allowed_file(
            file.filename
        ):

            return jsonify({

                "error":
                    "Unsupported file type."

            }), 400

        filename = secure_filename(
            file.filename
        )

        file_path = (
            UPLOAD_FOLDER
            / filename
        )

        file.save(
            file_path
        )

        print(
            f"Processing: "
            f"{file_path}"
        )

        document = load_document(
            file_path
        )

        file_type = (
            file_path.suffix.lower()
        )

        if file_type == ".csv":

            chunks = document

        else:

            chunks = text_splitter(
                document
            )

        print(
            f"Total chunks: "
            f"{len(chunks)}"
        )

        create_vector_store(
            chunks
        )

        document_uploaded = True

        return jsonify({

            "success":
                True,

            "message":
                f"{filename} uploaded "
                f"successfully. "
                f"{len(chunks)} chunks indexed."

        })

    except Exception as error:

        print(
            f"Upload error: "
            f"{error}"
        )

        return jsonify({

            "error":
                str(error)

        }), 500


@app.route(
    "/search",
    methods=["POST"]
)
def search():

    try:
        data = request.get_json()

        if not data:

            return jsonify({

                "error":
                    "Invalid request."

            }), 400

        query = data.get(
            "query"
        )

        if not query:

            return jsonify({

                "error":
                    "Please enter a search query."

            }), 400

        if not document_uploaded:

            return jsonify({

                "error":
                    "Please upload a document first."

            }), 400

        print(
            f"Search query: "
            f"{query}"
        )

        vector_store = (
            get_vector_store()
        )

        results = semantic_search(

            vector_store,

            query

        )

        print(
            f"Retrieved "
            f"{len(results)} "
            f"results."
        )

        answer = generate_answer(

            query,

            results

        )

        formatted_results = []

        for document, score in results:

            formatted_results.append({

                "content":
                    document.page_content,

                "source":
                    document.metadata.get(

                        "source",

                        "Unknown"

                    ),

                "score":
                    float(score)

            })

        return jsonify({

            "answer":
                answer,

            "results":
                formatted_results

        })

    except Exception as error:

        print(
            f"Search error: "
            f"{error}"
        )

        return jsonify({

            "error":
                str(error)

        }), 500


if __name__ == "__main__":

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000

    )
