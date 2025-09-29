from PyPDF2 import PdfReader
import os 
import traceback
import json
import re
import pandas as pd
from fpdf import FPDF


def read_file(file):
    try:
        if file.name.endswith(".pdf"):
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text

        elif file.name.endswith(".txt"):
            return file.read().decode("utf-8")

        else:
            raise ValueError("Unsupported file format. Only PDF and TXT files are supported.")
    
    except Exception as e:
        raise ValueError(f"Error reading the file: {str(e)}")


def get_table_data(first_quiz):
    try:
        quiz_table_data = []

        # 🧠 Bonus Tip: Extract JSON block if wrapped in markdown
        match = re.search(r"```json(.*?)```", first_quiz, re.DOTALL)
        if match:
            json_block = match.group(1).strip()
        else:
            json_block = first_quiz.strip()

        # Optional: Clean trailing commas if needed
        json_block = re.sub(r',\s*([}\]])', r'\1', json_block)

        # Parse JSON
        parsed_quiz = json.loads(json_block)

        # Build table data
        for key, value in parsed_quiz.items():
            mcq = value["mcq"]
            options = "|".join(
                [f"{option}:{option_value}" for option, option_value in value["options"].items()]
            )
            correct = value["correct"]
            quiz_table_data.append({
                "MCQ": mcq,
                "Choices": options,
                "Correct": correct
            })

        final_data = pd.DataFrame(quiz_table_data)
        return final_data

    

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
def generate_pdf(dataframe,title="MCQ report"):
    filename="mcq_report.pdf"
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=12)
    pdf.cell(200,10,txt=title,ln=True,align="C")
    pdf.ln(10)
    for index, row in dataframe.iterrows():
         pdf.multi_cell(0, 10, f"Q{index+1}: {row['MCQ']}")
         pdf.multi_cell(0, 10, f"Choices: {row['Choices']}")
         pdf.multi_cell(0, 10, f"Correct Answer: {row['Correct']}")
         pdf.ln(5)
    pdf.output(filename)
    return filename
