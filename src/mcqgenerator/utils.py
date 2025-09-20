from PyPDF2 import PdfReader
import os 
import traceback


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

def get_table_data(quiz_str) :
    try:
        quiz_table_data=[]
        for key,value in quiz_str.items():
            mcq= value["mcq"]
            options="|".join(
                [
                f"{option}:{option_value}"
                for option, option_value in value["options"].items()
                ]
            )
            correct= value["correct"]
            quiz_table_data.append({"MCQ":mcq,"Choices":options,"Correct":correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        return False
