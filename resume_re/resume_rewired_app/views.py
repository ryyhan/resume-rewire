import os
from django.shortcuts import render
import PyPDF2 as pdf
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
text = ""
jd = ""

def input_pdf_text(uploaded_file):
    global text
    reader = pdf.PdfReader(uploaded_file)
    for page in reader.pages:
        text += str(page.extract_text())
    return text

def get_response(input_text):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": input_text}],
        model="llama3-8b-8192",
        temperature=0.5,
        top_p=1,
        stop=None,
        stream=False,
    )
    return response.choices[0].message.content if response.choices else ""

def extract_percentage(response):
    match = re.search(r'(\d+)%', response)
    return match.group(1) if match else "No percentage found"

def smart_ats_view(request):
    global jd, text
    response = ""
    percentage = ""
    
    if request.method == "POST":
        jd = request.POST.get("job_description")
        uploaded_file = request.FILES.get("resume")
        
        if uploaded_file:
            text = input_pdf_text(uploaded_file)
            response = get_response(f"Resume = {text}, Job Description = {jd}")
            percentage = extract_percentage(response)
    
    return render(request, 'index.html', {
        'response': response,
        'percentage': percentage,
    })
