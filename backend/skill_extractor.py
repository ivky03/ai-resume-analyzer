import re

SKILL_KEYWORDS = [
    # Programming Languages
    "python", "java", "c++", "c#", "typescript", "javascript", "go", "rust", "kotlin", "ruby", "scala", "matlab", "r",

    # Data Science & ML
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "matplotlib", "seaborn", "xgboost", "lightgbm",
    "mlflow", "huggingface", "transformers", "statsmodels", "keras",

    # NLP / LLM
    "spacy", "nltk", "gensim", "bert", "gpt", "llama", "t5", "langchain", "openai", "llm", "vector db", "pinecone", "faiss", "chromadb",

    # Cloud
    "aws", "azure", "gcp", "google cloud", "sagemaker", "cloud functions", "lambda", "cloud run", "cloudflare", "firebase",

    # DevOps & MLOps
    "docker", "kubernetes", "jenkins", "gitlab", "github actions", "terraform", "ansible", "prometheus", "grafana", "airflow", "mlops",

    # Databases
    "mysql", "postgresql", "mongodb", "sqlite", "firebase", "snowflake", "bigquery", "dynamodb", "redis", "cassandra", "neo4j",

    # Web Development
    "react", "angular", "vue", "next.js", "django", "flask", "fastapi", "node.js", "express", "graphql", "bootstrap", "html", "css", "tailwind",

    # Mobile Development
    "flutter", "react native", "swift", "android studio", "ios", "kotlin",

    # Testing / CICD
    "pytest", "unittest", "selenium", "cypress", "junit", "ci/cd", "code coverage",

    # Security
    "cybersecurity", "pen testing", "owasp", "vulnerability scanning", "kali linux", "metasploit", "network security",

    # Version Control
    "git", "github", "gitlab", "bitbucket",

    # Other CS Concepts / Tools
    "linux", "bash", "shell scripting", "oop", "system design", "data structures", "algorithms", "rest", "api", "grpc", "json",
    "agile", "scrum", "jira", "notion", "postman", "figma", "trello"
]

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        # match whole word to avoid partial matches
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.append(skill)
    return sorted(list(set(found)))
