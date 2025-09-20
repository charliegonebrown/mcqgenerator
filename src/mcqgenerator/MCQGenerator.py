#All required imports
import os
import json
import traceback
import pandas as pd 
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import PyPDF2
import re
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file,get_table_data

#loading the environment variables 
load_dotenv()
#Access environment variable
key= os.getenv("GOOGLE_API_KEY")

#Initializing the model 

model=init_chat_model("gemini-2.5-flash", model_provider="google_genai")
#Defining the prompt templates 
prompt=ChatPromptTemplate.from_template(
    "Text:{text}"
    "You are an expert MCQ maker. Given the above text, it is your job to create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. Make sure the questions are not repeated and check all the questions to be conforming the text as well. "
    "Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. Ensure to make {number} MCQs {response_json} "
)
chain= prompt|model | StrOutputParser()

evaluation_prompt = ChatPromptTemplate.from_template(
    "You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students, "
    "you need to evaluate the complexity of the questions and give a complete analysis of the quiz. "
    "Only use at most 50 words for complexity analysis. "
    "If the quiz is not aligned with the cognitive and analytical abilities of the students, "
    "update the quiz questions that need improvement and adjust the tone to better suit the students' level. "
    "Quiz_MCQs:\n{quiz}\n\n"
    "Provide your expert evaluation and revised quiz below:"
)
eval_chain=evaluation_prompt|model|StrOutputParser()

