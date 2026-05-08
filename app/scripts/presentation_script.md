# CVMatchMaker — Presentation Script
## What to Say for Each Slide (approx 8–10 minutes total)

---

## Slide 1 — Title (30 seconds)
> "Hi everyone, my name is Saif Ali Khan and today I'm presenting my final year project called **CVMatchMaker**. It is a tool that uses Natural Language Processing to help job seekers understand why their CVs get rejected and what they can do to improve them."

---

## Slide 2 — Problem & Solution (1.5 minutes)
> "So what's the problem? When you apply for a job online, your CV doesn't go straight to a human. It goes through a computer system called an **ATS — Applicant Tracking System**. This system scans your CV for specific keywords. If those words aren't there, your CV gets rejected automatically — before anyone even reads it."
>
> "The tools that exist today, like Grammarly or TopCV, only fix spelling and grammar. They don't actually compare your CV against real job listings."
>
> "**CVMatchMaker solves this.** It uses content extraction to read your CV, applies NLP techniques to grab keywords, connects to the Reed.co.uk API to get real live job listings, and uses recommendation techniques to tell you exactly which skills you're missing. It gives you a score, learning resources, and even generates a cover letter."

---

## Slide 3 — How It Works: 3-Step Pipeline (2 minutes) ⭐ KEY SLIDE
> "Let me explain the three key techniques that power this project."
>
> "**Step 1 is Content Extraction.** When a user uploads a PDF or Word document, my code uses Python libraries — PyPDF2 for PDFs and python-docx for Word files — to extract the raw text. It then splits the text into sections like Skills, Experience, and Education by detecting common headings."
>
> "**Step 2 is NLP — Natural Language Processing.** I use a library called spaCy. It doesn't just do a simple keyword search. It works in three layers. Layer 1 uses regex pattern matching to find exact skill phrases like 'machine learning' or 'node.js'. Layer 2 uses lemmatisation — that means it understands that 'developing' and 'develop' are the same word. Layer 3 uses synonym normalisation — so it knows that 'reactjs' and 'react' are the same skill."
>
> "**Step 3 is Recommendations.** The system connects to the Reed.co.uk API to download real job listings. Then it compares the skills found in the CV against the skills employers are asking for using set operations — intersection for matched skills, difference for missing ones. It ranks the missing skills by frequency — how many jobs ask for them — and links each one to free courses on YouTube and Coursera."

---

## Slide 4 — Homepage (30 seconds)
> "This is the landing page. It has a simple message — 'Upload Your CV, See What's Missing' — with Login and Sign Up forms below."
>
> "All passwords are stored using **PBKDF2 hashing**, which is the industry standard. Even I as the developer cannot see anyone's password."

---

## Slide 5 — Dashboard (45 seconds)
> "After logging in, the user sees their Dashboard. This is where they upload their CV — either a PDF or a Word document. They type in the job they want, like 'Software Engineer', and optionally a city."
>
> "When they click Analyse, the system runs all three steps I just described — content extraction, NLP keyword grabbing, and the comparison against live job listings — all in a few seconds."

---

## Slide 6 — Results: Score & Skills (1.5 minutes)
> "This is the main results page. At the top, there's a **Career Score out of 100**. This is calculated by dividing the number of matched skills by the total skills employers are asking for."
>
> "The **green chips** are skills found on the user's CV using NLP. The **red chips** are skills that are missing. Each missing skill is tagged with a priority — High means more than 50% of job listings ask for it."
>
> "The system also provides links to **free courses** on YouTube and Coursera for each missing skill. And there's a button to add any skill to a personal Learning Path."

---

## Slide 7 — History & Compare (1 minute)
> "Every analysis the user does is saved in their History. There's a score trend chart at the top that shows if their scores are going up over time — which motivates them to keep improving."
>
> "I also built a **Compare feature**. The user can pick any two past analyses and see them side by side — scores, matched skills, and it even highlights any new skills they gained between the two analyses."

---

## Slide 8 — Learning Path (45 seconds)
> "The Learning Path is like a to-do list for skills. When the user sees a missing skill on the results page, they can click 'Add to Learning Path'."
>
> "Each skill has links to free courses. When they finish learning, they tick it off. There's a progress bar showing how many they've completed. All of this is saved in the database so it's always there when they log back in."

---

## Slide 9 — Tech Stack (1 minute)
> "Briefly on how it was built. The backend uses **Python with Flask**. The NLP skill extraction uses **spaCy**, which is a Natural Language Processing library — it tokenises text, applies lemmatisation, and extracts skill names using pattern matching."
>
> "Job data comes from the **Reed.co.uk API** — so the analysis is always based on real, current job listings."
>
> "The database is **SQLite** with three tables: Users, AnalysisSessions, and LearningGoals. Importantly, the actual CV file is **never saved** — it's processed in memory and deleted immediately. This is key for **GDPR compliance**."
>
> "The frontend is plain HTML, CSS, and JavaScript. No complex frameworks — I wanted to keep it simple and clean."

---

## Slide 10 — Thank You (15 seconds)
> "That's my project. Thank you for listening — I'm happy to take any questions."

---

### Tips for the Demo:
1. **Have the website open** in your browser before presenting
2. After Slide 5, **switch to the live website** and do a quick demo: upload a CV, show the results
3. Keep your voice steady and don't rush — the slides have bullet points, not paragraphs
4. If someone asks about "AI": say **"I use NLP techniques — specifically spaCy for tokenisation and lemmatisation, regex for pattern matching, and synonym normalisation — rather than a generic AI model."**
5. If someone asks about the database: **"3 tables — Users, Sessions, Goals. CVs are never stored."**
6. If someone asks about GDPR: **"CVs are processed in memory only and immediately deleted. Only scores and skills are saved."**
7. If someone asks about the 3 techniques: explain the pipeline — **Content Extraction → NLP Analysis → Recommendation via Set Comparison**
