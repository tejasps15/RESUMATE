import re


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    text = text.lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("/", " ")

    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# SKILL / KEYWORD DATABASE
# ============================================================

SKILL_GROUPS = {

    "programming": [
        "python",
        "c",
        "c++",
        "java",
        "sql"
    ],

    "engineering_software": [
        "matlab",
        "simulink",
        "autocad",
        "autocad electrical",
        "etap",
        "arduino ide",
        "git",
        "github"
    ],

    "power_systems": [
        "power systems",
        "power system",
        "power distribution",
        "power generation",
        "power evacuation",
        "transmission",
        "transmission networks",
        "substation",
        "switchyard",
        "grid reliability"
    ],

    "electrical_equipment": [
        "electrical machines",
        "transformer",
        "transformers",
        "generator",
        "generators",
        "switchgear",
        "electrical equipment"
    ],

    "protection": [
        "protection systems",
        "protection system",
        "relay protection",
        "relay",
        "relays",
        "protection"
    ],

    "electrical_analysis": [
        "circuit analysis",
        "electrical calculations",
        "electrical analysis",
        "power system analysis",
        "engineering analysis"
    ],

    "industrial": [
        "industrial operations",
        "industrial maintenance",
        "maintenance",
        "testing",
        "testing and commissioning",
        "troubleshooting",
        "industrial electrical"
    ],

    "embedded": [
        "embedded systems",
        "arduino",
        "esp32",
        "iot",
        "sensor interfacing",
        "microcontroller"
    ],

    "automation": [
        "plc",
        "scada",
        "industrial automation",
        "automation",
        "control systems"
    ],

    "soft_skills": [
        "problem solving",
        "problem-solving",
        "teamwork",
        "communication",
        "adaptability",
        "leadership"
    ]
}


# ============================================================
# FLATTEN SKILLS
# ============================================================

ALL_SKILLS = []

for group in SKILL_GROUPS.values():

    for skill in group:

        if skill not in ALL_SKILLS:
            ALL_SKILLS.append(skill)


# ============================================================
# ALIASES
# ============================================================

ALIASES = {

    "power system": "power systems",
    "power generation": "power generation",
    "transmission network": "transmission networks",

    "substations": "substation",

    "switchyards": "switchyard",

    "transformers": "transformer",

    "generators": "generator",

    "relays": "relay",

    "protection systems": "protection system",

    "matlab": "matlab",
    "simulink": "simulink",

    "electrical engineering": "electrical engineering",

    "eee": "electrical engineering",

    "electrical and electronics engineering":
        "electrical engineering",

    "electrical & electronics engineering":
        "electrical engineering"
}


# ============================================================
# PHRASE MATCHING
# ============================================================

def contains_skill(text, skill):

    skill = skill.lower()

    if skill in text:
        return True

    return False


# ============================================================
# EXTRACT REQUIRED SKILLS FROM JD
# ============================================================

def extract_required_skills(job):

    required = []

    for skill in ALL_SKILLS:

        if contains_skill(job, skill):

            required.append(skill)

    return list(dict.fromkeys(required))


# ============================================================
# MATCH RESUME AGAINST JD
# ============================================================

def match_skills(resume, required_skills):

    matching = []
    missing = []

    for skill in required_skills:

        if contains_skill(resume, skill):

            matching.append(skill)

        else:

            missing.append(skill)

    return matching, missing


# ============================================================
# IMPORTANT KEYWORDS
# ============================================================

def extract_important_keywords(job):

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z+#.-]{3,}\b",
        job
    )

    stop_words = {
        "this",
        "that",
        "with",
        "from",
        "your",
        "will",
        "have",
        "been",
        "into",
        "they",
        "their",
        "about",
        "candidate",
        "candidates",
        "looking",
        "using",
        "support",
        "assist",
        "work",
        "working",
        "team",
        "skills",
        "required",
        "preferred",
        "experience",
        "knowledge",
        "basic",
        "strong",
        "good",
        "ability",
        "degree",
        "engineering",
        "engineer"
    }

    keywords = []

    for word in words:

        word = word.lower()

        if word not in stop_words:

            if word not in keywords:

                keywords.append(word)

    return keywords


def keyword_match_score(
    resume,
    job,
    required_skills
):

    important_words = extract_important_keywords(
        job
    )

    matched_words = []

    for word in important_words:

        if word in resume:

            matched_words.append(word)

    if not important_words:

        return 0, []

    score = (
        len(matched_words)
        /
        len(important_words)
    ) * 100

    return round(score), matched_words


# ============================================================
# EXPERIENCE RELEVANCE
# ============================================================

def experience_relevance_score(resume):

    experience_terms = [

        "internship",
        "industrial training",
        "training",
        "project",
        "research",
        "publication",

        "thermal power",
        "power plant",
        "substation",
        "switchyard",

        "transformer",
        "protection",
        "transmission",

        "power systems",
        "electrical machines",

        "matlab",
        "simulink",
        "autocad"
    ]

    found = []

    for term in experience_terms:

        if term in resume:

            found.append(term)

    if not found:

        return 30

    score = min(
        100,
        40 + len(found) * 6
    )

    return score


# ============================================================
# EDUCATION MATCH
# ============================================================

def education_score(resume, job):

    electrical_resume = (
        "electrical engineering" in resume
        or
        "electrical & electronics engineering" in resume
        or
        "electrical and electronics engineering" in resume
    )

    electrical_job = (
        "electrical engineering" in job
        or
        "electrical & electronics engineering" in job
        or
        "electrical and electronics engineering" in job
    )

    if electrical_resume and electrical_job:

        return 100

    if "b.tech" in resume or "b.e" in resume:

        return 70

    return 50


# ============================================================
# RESUME STRUCTURE
# ============================================================

def structure_score(resume):

    sections = {

        "education": [
            "education",
            "academic"
        ],

        "skills": [
            "skills",
            "technical skills"
        ],

        "projects": [
            "projects",
            "project"
        ],

        "experience": [
            "experience",
            "internship",
            "industrial training"
        ],

        "certifications": [
            "certifications",
            "certification"
        ],

        "achievements": [
            "achievements",
            "achievement"
        ]
    }

    found_sections = 0

    for section_words in sections.values():

        found = False

        for word in section_words:

            if word in resume:

                found = True
                break

        if found:

            found_sections += 1

    score = (
        found_sections
        /
        len(sections)
    ) * 100

    return round(score)


# ============================================================
# RESUME QUALITY
# ============================================================

def quality_score(resume):

    word_count = len(
        resume.split()
    )

    if word_count >= 500:

        return 100

    elif word_count >= 400:

        return 95

    elif word_count >= 300:

        return 90

    elif word_count >= 200:

        return 80

    elif word_count >= 100:

        return 65

    else:

        return 40


# ============================================================
# FINAL ANALYZER
# ============================================================

def analyze_resume(
    resume_text,
    job_description
):

    resume = clean_text(
        resume_text
    )

    job = clean_text(
        job_description
    )

    # --------------------------------------------------------
    # REQUIRED SKILLS
    # --------------------------------------------------------

    required_skills = extract_required_skills(
        job
    )

    matching_skills, missing_skills = match_skills(
        resume,
        required_skills
    )

    if required_skills:

        skill_score = (
            len(matching_skills)
            /
            len(required_skills)
        ) * 100

    else:

        skill_score = 0


    # --------------------------------------------------------
    # KEYWORD SCORE
    # --------------------------------------------------------

    keyword_score, matched_keywords = (
        keyword_match_score(
            resume,
            job,
            required_skills
        )
    )


    # --------------------------------------------------------
    # EXPERIENCE SCORE
    # --------------------------------------------------------

    experience_score = (
        experience_relevance_score(
            resume
        )
    )


    # --------------------------------------------------------
    # EDUCATION SCORE
    # --------------------------------------------------------

    education_match = (
        education_score(
            resume,
            job
        )
    )


    # --------------------------------------------------------
    # STRUCTURE SCORE
    # --------------------------------------------------------

    completeness_score = (
        structure_score(
            resume
        )
    )


    # --------------------------------------------------------
    # QUALITY SCORE
    # --------------------------------------------------------

    quality = quality_score(
        resume
    )


    # --------------------------------------------------------
    # FINAL ATS SCORE
    # --------------------------------------------------------

    ats_score = (

        skill_score * 0.35

        +

        keyword_score * 0.20

        +

        experience_score * 0.20

        +

        education_match * 0.10

        +

        completeness_score * 0.10

        +

        quality * 0.05
    )


    ats_score = round(
        min(
            100,
            ats_score
        )
    )


    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return {

        "ats_score": ats_score,

        "skill_score": round(
            skill_score
        ),

        "keyword_score": round(
            keyword_score
        ),

        "experience_score": round(
            experience_score
        ),

        "education_score": round(
            education_match
        ),

        "completeness_score": round(
            completeness_score
        ),

        "quality_score": round(
            quality
        ),

        "matching_skills":
            matching_skills,

        "missing_skills":
            missing_skills,

        "matched_keywords":
            matched_keywords,

        "required_skills":
            required_skills
    }