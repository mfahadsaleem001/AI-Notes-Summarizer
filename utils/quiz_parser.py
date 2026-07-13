import re


def parse_quiz(quiz_text):

    questions = []

    blocks = re.split(r"Q\d+:", quiz_text)

    for block in blocks:

        block = block.strip()

        if not block:
            continue

        lines = [line.strip() for line in block.split("\n") if line.strip()]

        question = ""
        options = []
        answer = ""

        for line in lines:

            if line.startswith(("A)", "B)", "C)", "D)")):
                options.append(line)

            elif line.startswith("Correct Answer"):
                answer = line.replace("Correct Answer:", "").strip()

            elif question == "":
                question = line

        questions.append({
            "question": question,
            "options": options,
            "answer": answer
        })

    return questions