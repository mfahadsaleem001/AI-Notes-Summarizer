from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os


def export_summary_to_pdf(summary, output_folder="exports"):

    os.makedirs(output_folder, exist_ok=True)

    pdf_path = os.path.join(output_folder, "AI_Summary.pdf")

    document = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph("<b>AI Notes Summary</b>", styles["Title"])

    story.append(title)

    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    paragraphs = summary.split("\n")

    for line in paragraphs:

        if line.strip():

            story.append(
                Paragraph(line.replace("\n", "<br/>"), styles["BodyText"])
            )

    document.build(story)

    return pdf_path