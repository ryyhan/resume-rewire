import os
import streamlit as st
import PyPDF2 as pdf
from groq import Groq

from dotenv import load_dotenv
load_dotenv()
text=""
jd=""

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    global text
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

def get_repsonse(input):
    response = client.chat.completions.create(
    messages=system_settings,
    model="llama3-8b-8192",
    temperature=0.5,
    top_p=1,
    stop=None,
    stream=False,
)
    return response.choices[0].message.content

# Create the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"), )
input_prompt = """
Hey, act like a skilled and highly experienced ATS (Applicant Tracking System) with a deep understanding of various professional fields, including but not limited to tech, healthcare, finance, education, marketing, and more. Your task is to evaluate the resume based on the given job description.

Consider that the job market is very competitive, and you should provide the best assistance for improving the resume. Analyze the resume thoroughly and compare it with the job description to:

1. Assign a percentage matching score based on how well the resume aligns with the job description.
2. Identify missing keywords and skills that are important for the position.
3. Suggest improvements to make the resume more competitive for the specific role.

Please provide your analysis with high accuracy, considering both hard and soft skills, relevant experience, and any specific requirements mentioned in the job description.

Based on your analysis, please provide:
1. Percentage match between the resume and job description
2. List of missing keywords or skills
3. Suggestions for improving the resume
4. Any other relevant observations or recommendations
"""

system_settings = [
        {
            "role": "system",
            "content": input_prompt
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": f"Resume = {text}, Job Description = {jd}",
        }
    ]




## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")


if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_repsonse(input_prompt)
        st.write(response)





