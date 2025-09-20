import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from src.mcqgenerator.MCQGenerator import chain,eval_chain
from src.mcqgenerator.logger import logging

with open(r"c:\Users\odusa\mcqgenerator\RESPONSE.json","r") as file:
    RESPONSE_JSON = json.load(file)
#CReating the Title
st.title("MCQ Creator Application with Langchain")
#Creating a fore 
with st.form ("user_inputs"):
    #file upload
    uploaded_file= st.file_uploader("Upload your pdf or text file")
    #Input Fields
    mcq_count= st.number_input("No of MCQs",min_value=3, max_value=50)
    #Subject
    subject=st.text_input("Insert Subject",max_chars=20)
    #Creating Tone
    tone= st.text_input("Complexity Level of Questions",max_chars=20,placeholder="simple")
    #Add Button 
    button= st.form_submit_button("Create Mcqs")

    #Check if button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject:
        with st.spinner("Loading..."):
            try:
                # Read the uploaded file
                text = read_file(uploaded_file)

                # Prepare input variables for the first chain
                variables = {
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone":tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                }

                # Invoke the first chain to generate quiz
                firstquiz = chain.invoke(variables)
                st.write(firstquiz)

                # Prepare input for evaluation chain
                variable2 = {
                    "subject": subject,
                    "quiz": firstquiz
                }

                # Invoke the second chain
                sec_quiz = eval_chain.invoke(variable2)

                # Display the result Analysis
                st.write(sec_quiz)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
