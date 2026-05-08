# skills_data.py
# Curated skill dictionary for CVMatchMaker NLP matching
# Grouped by category for display purposes

SKILLS = {
    "Programming Languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "c", "go", "rust",
        "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "perl", "bash",
        "shell scripting", "powershell", "haskell", "lua"
    ],
    "Web Development": [
        "html", "css", "html5", "css3", "react", "reactjs", "react.js", "angular",
        "angularjs", "vue", "vue.js", "vuejs", "svelte", "next.js", "nextjs",
        "nuxt.js", "jquery", "bootstrap", "tailwind", "tailwindcss", "sass", "less",
        "webpack", "vite", "gatsby"
    ],
    "Backend & Frameworks": [
        "flask", "django", "fastapi", "express", "node.js", "nodejs", "spring",
        "spring boot", "laravel", "rails", "ruby on rails", "asp.net", "dotnet",
        ".net", "nestjs", "graphql", "rest", "restful", "rest api", "apis",
        "microservices"
    ],
    "Databases": [
        "sql", "mysql", "postgresql", "postgres", "sqlite", "mongodb", "redis",
        "elasticsearch", "cassandra", "dynamodb", "oracle", "mssql", "mariadb",
        "nosql", "firebase", "supabase"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s",
        "terraform", "ansible", "jenkins", "ci/cd", "github actions", "gitlab ci",
        "linux", "unix", "nginx", "apache", "heroku", "vercel", "netlify",
        "cloudflare", "devops"
    ],
    "Data & AI": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
        "sklearn", "pandas", "numpy", "matplotlib", "seaborn", "data analysis",
        "data science", "statistics", "tableau", "power bi", "spark", "hadoop",
        "etl", "data engineering", "data visualization"
    ],
    "Tools & Practices": [
        "git", "github", "gitlab", "jira", "agile", "scrum", "kanban",
        "test driven development", "tdd", "unit testing", "integration testing",
        "selenium", "jest", "pytest", "ci/cd", "code review", "pair programming",
        "version control", "object oriented", "oop"
    ],
    "Soft Skills": [
        "communication", "teamwork", "leadership", "problem solving", "critical thinking",
        "time management", "project management", "collaboration", "adaptability",
        "attention to detail", "analytical", "presentation"
    ]
}

# Flat list for quick lookup (lowercased)
ALL_SKILLS = []
for category, skill_list in SKILLS.items():
    for skill in skill_list:
        ALL_SKILLS.append(skill.lower())

# Synonyms — maps alternate terms to canonical skill name
SYNONYMS = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "node": "node.js",
    "react.js": "react",
    "reactjs": "react",
    "vue.js": "vue",
    "vuejs": "vue",
    "k8s": "kubernetes",
    "sklearn": "scikit-learn",
    "postgres": "postgresql",
    "mssql": "sql",
    "nosql": "mongodb",
    "dotnet": ".net",
    "asp.net": ".net",
    "gcp": "google cloud",
    "rest api": "rest",
    "restful": "rest",
    "apis": "rest",
    "oop": "object oriented",
    "tdd": "test driven development",
    "nlp": "natural language processing",
    "ci/cd": "devops",
    "machine learning": "machine learning",
    "deep learning": "deep learning",
}

# ─────────────────────────────────────────────────────────────────────────────
# Learning resources: skill → list of {title, provider, url, type}
# type can be: "Course", "Tutorial", "YouTube", "Docs", "Practice", "Certification"
# ─────────────────────────────────────────────────────────────────────────────
LEARNING_RESOURCES = {
    "python": [
        {"title": "Python Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/python/", "type": "Tutorial"},
        {"title": "Python for Everybody", "provider": "Coursera", "url": "https://www.coursera.org/specializations/python", "type": "Course"},
        {"title": "Python Tutorial for Beginners (Full Course)", "provider": "YouTube – Programming with Mosh", "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc", "type": "YouTube"},
    ],
    "javascript": [
        {"title": "JavaScript Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/js/", "type": "Tutorial"},
        {"title": "JavaScript Algorithms and Data Structures", "provider": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "type": "Course"},
        {"title": "JavaScript Full Course for Beginners", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=PkZNo7MFNFg", "type": "YouTube"},
    ],
    "typescript": [
        {"title": "TypeScript Handbook", "provider": "typescriptlang.org", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "type": "Docs"},
        {"title": "TypeScript Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/typescript/", "type": "Tutorial"},
        {"title": "TypeScript Course for Beginners", "provider": "YouTube – Academind", "url": "https://www.youtube.com/watch?v=BwuLxPH8IDs", "type": "YouTube"},
    ],
    "react": [
        {"title": "React Official Docs", "provider": "React", "url": "https://react.dev/learn", "type": "Docs"},
        {"title": "React Front End Development", "provider": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/front-end-development-libraries/", "type": "Course"},
        {"title": "React Course – Full Tutorial for Beginners", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=bMknfKXIFA8", "type": "YouTube"},
    ],
    "node.js": [
        {"title": "Node.js Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/nodejs/", "type": "Tutorial"},
        {"title": "Node.js Full Course for Beginners", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=RLtyhwFtXQA", "type": "YouTube"},
    ],
    "flask": [
        {"title": "Flask Official Tutorial", "provider": "Flask Docs", "url": "https://flask.palletsprojects.com/en/stable/tutorial/", "type": "Tutorial"},
        {"title": "Python Flask Tutorial – Full Course", "provider": "YouTube – Corey Schafer", "url": "https://www.youtube.com/watch?v=MwZwr5Tvyxo", "type": "YouTube"},
    ],
    "django": [
        {"title": "Django Official Tutorial", "provider": "djangoproject.com", "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/", "type": "Tutorial"},
        {"title": "Django Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/django/", "type": "Tutorial"},
        {"title": "Django Full Course for Beginners", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=F5mRW0jo-U4", "type": "YouTube"},
    ],
    "sql": [
        {"title": "SQL Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/sql/", "type": "Tutorial"},
        {"title": "SQL for Data Science", "provider": "Coursera", "url": "https://www.coursera.org/learn/sql-for-data-science", "type": "Course"},
        {"title": "SQL Tutorial – Full Database Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY", "type": "YouTube"},
    ],
    "postgresql": [
        {"title": "PostgreSQL Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/postgresql/", "type": "Tutorial"},
        {"title": "PostgreSQL Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=qw--VYLpxG4", "type": "YouTube"},
    ],
    "mongodb": [
        {"title": "MongoDB Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/mongodb/", "type": "Tutorial"},
        {"title": "MongoDB Crash Course", "provider": "YouTube – Traversy Media", "url": "https://www.youtube.com/watch?v=-56x56UppqQ", "type": "YouTube"},
    ],
    "aws": [
        {"title": "AWS Cloud Practitioner Essentials", "provider": "Coursera", "url": "https://www.coursera.org/learn/aws-fundamentals", "type": "Course"},
        {"title": "AWS Free Tier Practice", "provider": "AWS", "url": "https://aws.amazon.com/free/", "type": "Practice"},
        {"title": "AWS Certified Cloud Practitioner – Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=SOTamWNgDKc", "type": "YouTube"},
    ],
    "azure": [
        {"title": "Azure Fundamentals AZ-900", "provider": "Microsoft Learn", "url": "https://learn.microsoft.com/en-us/certifications/azure-fundamentals/", "type": "Certification"},
        {"title": "Microsoft Azure Fundamentals – Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=NKEFWyqJ5XA", "type": "YouTube"},
    ],
    "docker": [
        {"title": "Docker for Beginners", "provider": "freeCodeCamp", "url": "https://www.freecodecamp.org/news/the-docker-handbook/", "type": "Tutorial"},
        {"title": "Play with Docker", "provider": "Docker", "url": "https://labs.play-with-docker.com/", "type": "Practice"},
        {"title": "Docker Tutorial for Beginners – Full Course", "provider": "YouTube – TechWorld with Nana", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "type": "YouTube"},
    ],
    "kubernetes": [
        {"title": "Kubernetes Basics", "provider": "kubernetes.io", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "type": "Tutorial"},
        {"title": "Kubernetes Course for Beginners", "provider": "YouTube – TechWorld with Nana", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "type": "YouTube"},
    ],
    "machine learning": [
        {"title": "Machine Learning Specialization", "provider": "Coursera (Andrew Ng)", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "type": "Course"},
        {"title": "Machine Learning Full Course", "provider": "YouTube – Simplilearn", "url": "https://www.youtube.com/watch?v=GwIo3gDZCVQ", "type": "YouTube"},
    ],
    "deep learning": [
        {"title": "Deep Learning Specialization", "provider": "Coursera (Andrew Ng)", "url": "https://www.coursera.org/specializations/deep-learning", "type": "Course"},
        {"title": "Deep Learning with Python – Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=VyWAvY2CF9c", "type": "YouTube"},
    ],
    "natural language processing": [
        {"title": "NLP with Python – Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=X2vAabgKiWM", "type": "YouTube"},
        {"title": "NLP Specialization", "provider": "Coursera (deeplearning.ai)", "url": "https://www.coursera.org/specializations/natural-language-processing", "type": "Course"},
    ],
    "tensorflow": [
        {"title": "TensorFlow Tutorials", "provider": "tensorflow.org", "url": "https://www.tensorflow.org/tutorials", "type": "Tutorial"},
        {"title": "TensorFlow 2.0 Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=tPYj3fFJGjk", "type": "YouTube"},
    ],
    "pytorch": [
        {"title": "PyTorch Tutorials", "provider": "pytorch.org", "url": "https://pytorch.org/tutorials/", "type": "Tutorial"},
        {"title": "PyTorch for Deep Learning – Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=V_xro1bcAuA", "type": "YouTube"},
    ],
    "scikit-learn": [
        {"title": "Scikit-learn Tutorial", "provider": "scikit-learn.org", "url": "https://scikit-learn.org/stable/tutorial/basic/tutorial.html", "type": "Tutorial"},
        {"title": "Machine Learning with Scikit-learn", "provider": "YouTube – Corey Schafer", "url": "https://www.youtube.com/watch?v=0B5eIE_1vpU", "type": "YouTube"},
    ],
    "pandas": [
        {"title": "Pandas Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/python/pandas/", "type": "Tutorial"},
        {"title": "Pandas & Python for Data Analysis", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=gtjxAH8uaP0", "type": "YouTube"},
    ],
    "git": [
        {"title": "Git Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/git/", "type": "Tutorial"},
        {"title": "Git and GitHub for Beginners – Crash Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "type": "YouTube"},
    ],
    "github": [
        {"title": "GitHub Docs – Getting Started", "provider": "GitHub", "url": "https://docs.github.com/en/get-started", "type": "Docs"},
        {"title": "Git and GitHub – Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "type": "YouTube"},
    ],
    "agile": [
        {"title": "Agile Fundamentals", "provider": "FutureLearn", "url": "https://www.futurelearn.com/courses/agile-projects", "type": "Course"},
        {"title": "Agile Methodology – Full Course", "provider": "YouTube – Simplilearn", "url": "https://www.youtube.com/watch?v=8eVXTyIZ1Hs", "type": "YouTube"},
    ],
    "devops": [
        {"title": "DevOps Roadmap for Beginners", "provider": "YouTube – TechWorld with Nana", "url": "https://www.youtube.com/watch?v=0yWAtQ6wYNM", "type": "YouTube"},
        {"title": "DevOps Fundamentals", "provider": "FutureLearn", "url": "https://www.futurelearn.com/courses/devops-fundamentals", "type": "Course"},
    ],
    "linux": [
        {"title": "Linux Command Line – Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=ZtqBQ68cfJc", "type": "YouTube"},
        {"title": "Linux Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/whatis/whatis_linux.asp", "type": "Tutorial"},
    ],
    "html": [
        {"title": "HTML Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/html/", "type": "Tutorial"},
        {"title": "HTML Full Course – Build a Website Tutorial", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=pQN-pnXPaVg", "type": "YouTube"},
    ],
    "css": [
        {"title": "CSS Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/css/", "type": "Tutorial"},
        {"title": "CSS Full Course – Flexbox and Grid", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=1Rs2ND1ryYc", "type": "YouTube"},
    ],
    "html5": [
        {"title": "HTML Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/html/", "type": "Tutorial"},
        {"title": "HTML5 Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=pQN-pnXPaVg", "type": "YouTube"},
    ],
    "data science": [
        {"title": "Data Science Specialization", "provider": "Coursera (Johns Hopkins)", "url": "https://www.coursera.org/specializations/jhu-data-science", "type": "Course"},
        {"title": "Data Science Full Course", "provider": "YouTube – Simplilearn", "url": "https://www.youtube.com/watch?v=-ETQ97mXXF0", "type": "YouTube"},
    ],
    "data analysis": [
        {"title": "Data Analysis with Python", "provider": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/", "type": "Course"},
        {"title": "Data Analysis with Python – Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=r-uOLxNrNk8", "type": "YouTube"},
    ],
    "java": [
        {"title": "Java Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/java/", "type": "Tutorial"},
        {"title": "Java Full Course for Beginners", "provider": "YouTube – Programming with Mosh", "url": "https://www.youtube.com/watch?v=eIrMbAQSU34", "type": "YouTube"},
    ],
    "c++": [
        {"title": "C++ Tutorial", "provider": "W3Schools", "url": "https://www.w3schools.com/cpp/", "type": "Tutorial"},
        {"title": "C++ Tutorial for Beginners – Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y", "type": "YouTube"},
    ],
    "leadership": [
        {"title": "Leadership and Emotional Intelligence", "provider": "Coursera", "url": "https://www.coursera.org/learn/leadership-emotional-intelligence", "type": "Course"},
        {"title": "Leadership Skills – How to Be a Good Leader", "provider": "YouTube – Practical Psychology", "url": "https://www.youtube.com/watch?v=nuYLt31Iuu0", "type": "YouTube"},
    ],
    "project management": [
        {"title": "Google Project Management Certificate", "provider": "Coursera", "url": "https://www.coursera.org/professional-certificates/google-project-management", "type": "Certification"},
        {"title": "Project Management Full Course", "provider": "YouTube – Simplilearn", "url": "https://www.youtube.com/watch?v=GC7pN8Mjot8", "type": "YouTube"},
    ],
    "communication": [
        {"title": "Communication Skills – Business English", "provider": "Coursera", "url": "https://www.coursera.org/learn/communication-management", "type": "Course"},
        {"title": "How to Improve Communication Skills", "provider": "YouTube – Practical Psychology", "url": "https://www.youtube.com/watch?v=HAnw168huqA", "type": "YouTube"},
    ],
    "unit testing": [
        {"title": "Unit Testing in Python – Full Course", "provider": "YouTube – Corey Schafer", "url": "https://www.youtube.com/watch?v=6tNS--WetLI", "type": "YouTube"},
        {"title": "Python Testing with pytest", "provider": "Real Python", "url": "https://realpython.com/pytest-python-testing/", "type": "Tutorial"},
    ],
    "fastapi": [
        {"title": "FastAPI Official Tutorial", "provider": "fastapi.tiangolo.com", "url": "https://fastapi.tiangolo.com/tutorial/", "type": "Tutorial"},
        {"title": "FastAPI Full Course for Beginners", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=7t2alSnE2-I", "type": "YouTube"},
    ],
    "graphql": [
        {"title": "GraphQL Full Course", "provider": "YouTube – freeCodeCamp", "url": "https://www.youtube.com/watch?v=ed8SzALpx1Q", "type": "YouTube"},
        {"title": "GraphQL Tutorial", "provider": "graphql.org", "url": "https://graphql.org/learn/", "type": "Tutorial"},
    ],
    "redis": [
        {"title": "Redis Crash Course", "provider": "YouTube – Traversy Media", "url": "https://www.youtube.com/watch?v=jgpVdJB2sKQ", "type": "YouTube"},
    ],
    "power bi": [
        {"title": "Power BI Tutorial for Beginners", "provider": "YouTube – Guy in a Cube", "url": "https://www.youtube.com/watch?v=AGrl-H87pRU", "type": "YouTube"},
        {"title": "Microsoft Power BI – Full Course", "provider": "Coursera", "url": "https://www.coursera.org/learn/microsoft-power-bi-desktop", "type": "Course"},
    ],
    "tableau": [
        {"title": "Tableau Full Course for Beginners", "provider": "YouTube – Simplilearn", "url": "https://www.youtube.com/watch?v=aHaOIvR00So", "type": "YouTube"},
    ],
    "scrum": [
        {"title": "Scrum Guide (Official)", "provider": "Scrum.org", "url": "https://www.scrum.org/resources/scrum-guide", "type": "Docs"},
        {"title": "Agile Scrum Full Course", "provider": "YouTube – Simplilearn", "url": "https://www.youtube.com/watch?v=gy1c4_YixCo", "type": "YouTube"},
    ],
    # ── Default fallback (used when no specific resource exists) ──
    "default": [
        {"title": "Search Coursera Courses", "provider": "Coursera", "url": "https://www.coursera.org/search", "type": "Course"},
        {"title": "Search FutureLearn Courses", "provider": "FutureLearn", "url": "https://www.futurelearn.com/search", "type": "Course"},
        {"title": "Search YouTube Tutorials", "provider": "YouTube", "url": "https://www.youtube.com/results?search_query=", "type": "YouTube"},
    ]
}
