# 📄 Resume ↔ Job Description Matcher

An NLP web app that scores how well your resume matches a job description and highlights the skills you're missing, so you can tailor your resume before applying.

🔗 **Live demo:** [resume-matcherz.streamlit.app](https://resume-matcherz.streamlit.app/)

---

## ✨ Features

- **Semantic match score** (0–100%) between a resume and a job description
- **Skill gap detection**: shows which skills the JD asks for that your resume already covers, and which are missing
- **PDF resume upload** with automatic text extraction
- **Clean Streamlit UI** with a color-coded score and skill "pills"

## 🧠 How It Works

1. **Text extraction:** the resume PDF is parsed with `PyPDF2` and cleaned (lowercased, whitespace collapsed).
2. **Embeddings:** the resume and job description are each converted into a vector using the `all-MiniLM-L6-v2` model from `sentence-transformers`. Embeddings capture *meaning*, so "built predictive models" and "developed machine learning algorithms" are recognized as similar even without shared keywords.
3. **Similarity score:** cosine similarity between the two vectors gives the match percentage.
4. **Skill gap analysis:** a predefined list of common technical skills is checked against both texts to find skills mentioned in the JD but absent from the resume.

## 🛠️ Tech Stack

| Area | Tools |
|---|---|
| Language | Python |
| NLP / ML | sentence-transformers, scikit-learn, NumPy |
| PDF parsing | PyPDF2 |
| Web app | Streamlit |
| Deployment | Streamlit Community Cloud |

## 🚀 Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/ShubhGuPTA-cmd/resume-matcher.git
cd resume-matcher

# 2. Create and activate a virtual environment
python -m venv venv
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the app
streamlit run app.py
```

The app opens at `http://localhost:8501`. The first run downloads the embedding model (~80 MB), which is a one-time step.

## 📁 Project Structure

```
resume-matcher/
├── app.py            # Streamlit UI
├── extract.py        # PDF text extraction and cleaning
├── matcher.py        # Embeddings, similarity score, skill-gap logic
├── requirements.txt  # Python dependencies
└── .gitignore
```

## ⚠️ Limitations

- The skill list is predefined, so skills outside it won't be detected.
- The match score is a semantic-similarity signal, not a prediction of hiring outcomes or ATS behavior.
- Scanned/image-only PDFs aren't supported, since text extraction needs a text-based PDF.

## 🔮 Future Improvements

- Automatic skill extraction (e.g. KeyBERT or NER) instead of a fixed list
- Section-wise scoring (projects, skills, experience)
- Suggested rewrite tips for weak sections
- Support for DOCX resumes

## 👤 Author

**Shubh Gupta**: B.Tech CSE (AI & ML), SRM Institute of Science and Technology
[GitHub](https://github.com/ShubhGuPTA-cmd)
