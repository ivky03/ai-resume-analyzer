from fastapi import FastAPI, File, UploadFile, Form
from resume_parser import extract_resume_text
from rag_pipeline import find_similar_jobs
from gemini_llm import generate_recommendations, generate_learning_plan
from skill_extractor import extract_skills  # new utility

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is up and running!"}

@app.post("/analyze-resume/")
async def analyze_resume(
    file: UploadFile = File(...),
    job_type: str = Form(...)
):
    try:
        print("[LOG] Received resume file")
        with open("temp_resume.pdf", "wb") as f:
            f.write(await file.read())

        print("[LOG] Parsing resume...")
        resume_text = extract_resume_text("temp_resume.pdf")
        print("[LOG] Resume text extracted.")

        print("[LOG] Running RAG matching...")
        matched_jobs = find_similar_jobs(resume_text, job_type)
        print("[LOG] Job matching done.")

        # 🔍 Skill Extraction
        print("[LOG] Extracting skills...")
        resume_skills = extract_skills(resume_text)

        job_descriptions = [job["description"] for job in matched_jobs]
        job_skills = set()
        for desc in job_descriptions:
            job_skills.update(extract_skills(desc))

        missing_skills = list(set(job_skills) - set(resume_skills))
        print(f"[LOG] Missing skills: {missing_skills}")

        # 🧠 Get LLM feedback
        print("[LOG] Calling Gemini for feedback...")
        feedback = generate_recommendations(resume_text, matched_jobs, job_type)

        # 📘 Get learning plan
        print("[LOG] Calling Gemini for learning plan...")
        learning_plan = generate_learning_plan(missing_skills, job_type)


        return {
            "matched_jobs": matched_jobs,
            "llm_feedback": feedback,
            "skill_gaps": missing_skills,
            "learning_path": learning_plan
        }

    except Exception as e:
        print("[ERROR]", e)
        return {"error": str(e)}
