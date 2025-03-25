import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Load job data
with open('data/job_data.json') as f:
    job_data = json.load(f)

job_embeddings = np.load('data/job_embeddings.npy')

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
def is_match(job, job_type):
    title = job["title"].lower()
    if job_type.lower() == "internship":
        return "intern" in title or "trainee" in title or "assistant" in title
    else:
        # Exclude internships from full-time roles
        return not any(word in title for word in ["intern", "trainee", "assistant"])



def find_similar_jobs(resume_text, job_type="Full-Time", top_k=3):
    # Load job data and filter by job_type
    filtered_jobs = [job for job in job_data if is_match(job, job_type)]
    
    if not filtered_jobs:
        return [{"title": "No matching jobs found", "description": "", "score": 0.0}]

    # Get just descriptions
    descriptions = [job["description"] for job in filtered_jobs]

    # Embed resume
    resume_embedding = model.encode([resume_text])
    job_desc_embeddings = model.encode(descriptions)

    scores = cosine_similarity(resume_embedding, job_desc_embeddings)[0]
    top_indices = scores.argsort()[-top_k:][::-1]

    matches = []
    for idx in top_indices:
        job = filtered_jobs[idx]
        matches.append({
            "title": job["title"],
            "description": job["description"],
            "score": float(round(scores[idx], 3))
        })

    return matches

