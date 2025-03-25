import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def generate_recommendations(resume_text, matched_jobs, job_type):
    job_list = "\n".join(
        [f"- {j['title']} (Score: {j['score']})" for j in matched_jobs]
    )

    prompt = f"""
You are a career coach helping students and recent graduates improve their resumes and career direction.

Resume Type: {job_type}

Here is the user's resume:
{resume_text}

Here are the top matched jobs based on similarity:
{job_list}

Please return a concise, structured response with the following **3 sections only**:

---

**1. Overall Impression**  
A short, encouraging sentence on how the resume aligns with the job role. Do NOT give a score.

**2. Top 3 Suggestions to Improve the Resume**  
- Use bullet points. Be constructive and specific.  
- Focus on impact, clarity, and alignment with job roles.

**3. Career Direction Based on This Resume + Jobs**  
- Suggest one likely role that fits the resume  
- Include a 1–2 line rationale and a clear next step

Use Markdown formatting. Be positive and student-friendly. Limit the total output to under 200 words.
"""


    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = httpx.post(GEMINI_URL, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        content = response.json()
        return content['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Gemini API error: {e}"


def generate_learning_plan(missing_skills, job_type="Data Scientist"):
    if not missing_skills:
        prompt = f"""
The user's resume aligns well with the target job role: {job_type}.

Please suggest 2–3 **advanced or emerging skills** they can learn to grow in this career path.

For each skill:
1. Recommend a short learning path (2–3 steps)
2. Suggest an online course (Coursera, Udemy, edX, or YouTube)
3. Include the course link if possible

🚫 DO NOT ask the user for more information. Just assume they have basic experience in {job_type}-related skills like Python and SQL.
✅ Respond in Markdown format. Be student-friendly and clear.
"""
    else:
        prompt = f"""
The user is applying for a {job_type} role and is missing the following key skills: {', '.join(missing_skills)}.

For each skill:
1. Suggest a brief learning path (2–3 steps)
2. Recommend a current online course (Coursera, Udemy, edX, YouTube)
3. Include a course link if possible

Be friendly for beginners. Use Markdown formatting. Do NOT ask follow-up questions.
"""

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = httpx.post(GEMINI_URL, headers=headers, json=payload, timeout=40.0)
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Gemini API error: {e}"
