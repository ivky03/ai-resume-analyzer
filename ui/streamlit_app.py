import streamlit as st
import requests

st.title("🤖 ResumeGPT: Smart Job Matcher + Skill Gap Coach")

# Upload resume
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
job_type = st.selectbox(
    "What type of role are you looking for?",
    ("Full-Time", "Internship")
)

if uploaded_file:
    st.success("Resume uploaded successfully!")

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            data = {"job_type": job_type}
            response = requests.post(
                "http://127.0.0.1:8000/analyze-resume/", files=files,
    data=data
            )

            if response.status_code == 200:
                data = response.json()

                if "matched_jobs" in data and "llm_feedback" in data:
                    st.subheader("📌 Top Job Matches:")
                    for job in data["matched_jobs"]:
                        st.markdown(f"{job['title']}")
                        st.write(job["description"])
                        st.markdown("---")

                    st.subheader("🧠 LLM Feedback:")
                    st.markdown(data["llm_feedback"])
                

                if "learning_path" in data:
                    st.subheader("📘 Personalized Learning Plan:")
                    st.markdown(data["learning_path"])
                else:
                    st.error("Backend returned unexpected response.")
                    st.json(data)
            else:
                st.error("Failed to analyze resume.")
                st.text(f"Status Code: {response.status_code}")
                st.text(f"Response: {response.text}")
