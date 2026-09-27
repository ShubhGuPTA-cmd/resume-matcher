from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load once, reuse for every comparison
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """Convert text into a numeric vector representing its meaning."""
    return model.encode([text])[0]

def compute_similarity(resume_text, jd_text):
    """Return a 0-100 match score between resume and job description."""
    resume_emb = get_embedding(resume_text)
    jd_emb = get_embedding(jd_text)

    score = cosine_similarity([resume_emb], [jd_emb])[0][0]
    return round(score * 100, 1)

# A starter list — expand this with skills relevant to your target roles
COMMON_SKILLS = [
    "python", "java", "sql", "mysql", "javascript", "react", "node.js",
    "machine learning", "deep learning", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "aws", "docker", "kubernetes",
    "git", "rest api", "flask", "django", "html", "css", "excel",
    "data analysis", "data visualization", "nlp", "computer vision"
]

def find_missing_skills(resume_text, jd_text, skill_list=COMMON_SKILLS):
    """Find skills mentioned in the JD but not in the resume."""
    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()

    jd_skills = [s for s in skill_list if s in jd_lower]
    missing = [s for s in jd_skills if s not in resume_lower]

    return jd_skills, missing