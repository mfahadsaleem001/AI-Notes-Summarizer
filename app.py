from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from utils.quiz_parser import parse_quiz
import os

from utils.pdf_reader import read_pdf
from utils.docx_reader import read_docx
from utils.txt_reader import read_txt

from utils.summarizer import summarize_text
from utils.quiz_generator import generate_quiz
from utils.flashcard_generator import generate_flashcards
from utils.viva_generator import generate_viva

from utils.pdf_export import export_summary_to_pdf
from utils.docx_export import export_summary_to_docx

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store latest summary
latest_summary = ""
latest_quiz = ""
latest_flashcards = ""
latest_viva = ""
latest_filename = ""


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():

    global latest_summary, latest_quiz, latest_flashcards, latest_viva, latest_filename

    if request.method == "POST":

        if "notes" not in request.files:
            return "No file selected."

        file = request.files["notes"]

        if file.filename == "":
            return "Please select a file."

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(filepath)

            extension = filename.rsplit(".", 1)[1].lower()

            if extension == "pdf":
                text = read_pdf(filepath)

            elif extension == "docx":
                text = read_docx(filepath)

            elif extension == "txt":
                text = read_txt(filepath)

            else:
                return "Unsupported File."

            summary_mode = request.form.get("summary_mode")
            quiz_count = int(request.form.get("quiz_count", 5))

            summary = summarize_text(
                text,
                summary_mode
            )

            quiz = generate_quiz(text, total_questions=quiz_count)
            quiz_data = parse_quiz(quiz)

            latest_summary = summary
            latest_quiz = quiz
            latest_filename = filename

            quiz_data = parse_quiz(quiz)

            return render_template(
                "result.html",
                filename=filename,
                filesize=round(os.path.getsize(filepath) / 1024, 2),
                filetype=extension.upper(),
                summary=summary,
                quiz=quiz,
                quiz_data=quiz_data,
                summary_mode=summary_mode
            )

        return "Invalid File Type."
    
    return render_template("index.html")


@app.route("/download/pdf")
def download_pdf():

    global latest_summary

    if not latest_summary:
        return "No summary available. Please upload a file first."

    pdf_path = export_summary_to_pdf(latest_summary)

    return send_file(
        pdf_path,
        as_attachment=True
    )


@app.route("/download/docx")
def download_docx():

    global latest_summary

    if not latest_summary:
        return "No summary available. Please upload a file first."

    docx_path = export_summary_to_docx(latest_summary)

    return send_file(
        docx_path,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)