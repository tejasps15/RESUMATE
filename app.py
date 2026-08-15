import streamlit as st
from resume_parser import extract_text_from_resume
from analyzer import analyze_resume

from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RESUMATE | Resume & Career Intelligence",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# CAREER DATABASE
# ============================================================

CAREER_DATA = {

    "Computer Science & IT": {
        "roles": [
            "Software Engineer",
            "Python Developer",
            "Java Developer",
            "Full Stack Developer",
            "Backend Developer",
            "Frontend Developer",
            "Data Analyst",
            "Data Scientist",
            "Machine Learning Engineer",
            "AI Engineer",
            "DevOps Engineer",
            "Cloud Engineer",
            "Cybersecurity Analyst",
            "QA Engineer",
            "Automation Test Engineer"
        ],
        "keywords": [
            "python",
            "java",
            "c++",
            "sql",
            "git",
            "github",
            "linux",
            "docker",
            "aws",
            "azure",
            "javascript",
            "react",
            "node",
            "machine learning",
            "data structures",
            "algorithms"
        ]
    },

    "Electronics & Communication": {
        "roles": [
            "Electronics Engineer",
            "Embedded Systems Engineer",
            "VLSI Engineer",
            "Firmware Engineer",
            "IoT Engineer",
            "Hardware Engineer",
            "PCB Design Engineer",
            "RF Engineer",
            "Verification Engineer",
            "Automation Engineer"
        ],
        "keywords": [
            "embedded systems",
            "c",
            "c++",
            "microcontroller",
            "arduino",
            "esp32",
            "matlab",
            "simulink",
            "verilog",
            "vhdl",
            "pcb",
            "iot",
            "communication",
            "electronics"
        ]
    },

    "Electrical & Electronics": {
        "roles": [
            "Electrical Engineer",
            "Electrical Design Engineer",
            "Power Systems Engineer",
            "Power Electronics Engineer",
            "Control Systems Engineer",
            "Protection Engineer",
            "Automation Engineer",
            "Maintenance Engineer",
            "Testing & Commissioning Engineer",
            "Graduate Engineer Trainee"
        ],
        "keywords": [
            "power systems",
            "electrical machines",
            "transformer",
            "matlab",
            "simulink",
            "autocad",
            "autocad electrical",
            "etap",
            "plc",
            "scada",
            "switchgear",
            "protection relays",
            "electrical design",
            "power electronics"
        ]
    },

    "Mechanical Engineering": {
        "roles": [
            "Mechanical Design Engineer",
            "Production Engineer",
            "Manufacturing Engineer",
            "Maintenance Engineer",
            "Quality Engineer",
            "Automotive Engineer",
            "CAD Engineer",
            "CAE Engineer",
            "Thermal Engineer",
            "Graduate Engineer Trainee"
        ],
        "keywords": [
            "autocad",
            "solidworks",
            "catia",
            "ansys",
            "cad",
            "cam",
            "manufacturing",
            "production",
            "automobile",
            "thermodynamics",
            "mechanical design",
            "gd&t"
        ]
    },

    "Civil Engineering": {
        "roles": [
            "Civil Engineer",
            "Structural Engineer",
            "Site Engineer",
            "Planning Engineer",
            "Quantity Surveyor",
            "Design Engineer",
            "Construction Engineer",
            "Project Engineer",
            "Geotechnical Engineer",
            "Graduate Engineer Trainee"
        ],
        "keywords": [
            "autocad",
            "revit",
            "staad pro",
            "civil 3d",
            "structural",
            "construction",
            "quantity surveying",
            "project planning",
            "concrete",
            "steel design",
            "estimation"
        ]
    },

    "Chemical Engineering": {
        "roles": [
            "Process Engineer",
            "Production Engineer",
            "Chemical Engineer",
            "Process Safety Engineer",
            "Quality Engineer",
            "Plant Engineer",
            "Operations Engineer",
            "Research Engineer"
        ],
        "keywords": [
            "process engineering",
            "process safety",
            "aspen",
            "hysys",
            "chemical process",
            "thermodynamics",
            "mass transfer",
            "heat transfer",
            "production",
            "quality"
        ]
    },

    "Aerospace Engineering": {
        "roles": [
            "Aerospace Engineer",
            "Design Engineer",
            "Flight Systems Engineer",
            "Avionics Engineer",
            "Aerodynamics Engineer",
            "Manufacturing Engineer",
            "Structures Engineer",
            "Graduate Engineer Trainee"
        ],
        "keywords": [
            "aerospace",
            "catia",
            "solidworks",
            "ansys",
            "matlab",
            "simulink",
            "aerodynamics",
            "structures",
            "avionics",
            "manufacturing"
        ]
    },

    "Biotechnology": {
        "roles": [
            "Bioprocess Engineer",
            "Research Associate",
            "Quality Control Analyst",
            "Quality Assurance Associate",
            "Clinical Research Associate",
            "Bioinformatics Analyst",
            "Laboratory Analyst"
        ],
        "keywords": [
            "biotechnology",
            "bioprocess",
            "cell culture",
            "pcr",
            "bioinformatics",
            "laboratory",
            "quality control",
            "quality assurance",
            "research"
        ]
    },

    "Information Science": {
        "roles": [
            "Software Engineer",
            "Web Developer",
            "Data Analyst",
            "Data Engineer",
            "Cloud Engineer",
            "DevOps Engineer",
            "Cybersecurity Analyst",
            "QA Engineer",
            "Business Analyst"
        ],
        "keywords": [
            "python",
            "java",
            "sql",
            "javascript",
            "react",
            "git",
            "cloud",
            "aws",
            "azure",
            "data",
            "linux",
            "cybersecurity"
        ]
    },

    "AI & Machine Learning": {
        "roles": [
            "Machine Learning Engineer",
            "AI Engineer",
            "Data Scientist",
            "NLP Engineer",
            "Computer Vision Engineer",
            "AI Research Intern",
            "Data Analyst",
            "MLOps Engineer"
        ],
        "keywords": [
            "python",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "pandas",
            "numpy",
            "nlp",
            "computer vision",
            "sql",
            "data science"
        ]
    },

    "Management & Business": {
        "roles": [
            "Business Analyst",
            "Product Analyst",
            "Project Coordinator",
            "Operations Analyst",
            "Marketing Analyst",
            "HR Analyst",
            "Business Development Executive",
            "Management Trainee"
        ],
        "keywords": [
            "excel",
            "power bi",
            "tableau",
            "sql",
            "analytics",
            "communication",
            "leadership",
            "project management",
            "business analysis",
            "market research"
        ]
    },

    "Data & Analytics": {
        "roles": [
            "Data Analyst",
            "Data Scientist",
            "Business Intelligence Analyst",
            "Data Engineer",
            "Analytics Engineer",
            "Product Analyst",
            "Reporting Analyst"
        ],
        "keywords": [
            "python",
            "sql",
            "excel",
            "power bi",
            "tableau",
            "pandas",
            "numpy",
            "statistics",
            "data analysis",
            "machine learning"
        ]
    }
}


# ============================================================
# ROLE KEYWORDS
# ============================================================

ROLE_KEYWORDS = {}

for domain_data in CAREER_DATA.values():

    for role in domain_data["roles"]:

        ROLE_KEYWORDS[role] = list(
            dict.fromkeys(
                domain_data["keywords"] + [role.lower()]
            )
        )


ROLE_KEYWORDS.update({

    "Software Engineer": [
        "python",
        "java",
        "c++",
        "sql",
        "git",
        "data structures",
        "algorithms"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "statistics",
        "data analysis"
    ],

    "Machine Learning Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "scikit-learn"
    ],

    "Embedded Systems Engineer": [
        "c",
        "c++",
        "embedded systems",
        "microcontroller",
        "arduino",
        "esp32",
        "rtos"
    ],

    "Electrical Engineer": [
        "power systems",
        "electrical machines",
        "transformer",
        "matlab",
        "autocad",
        "electrical design"
    ],

    "Power Systems Engineer": [
        "power systems",
        "etap",
        "matlab",
        "simulink",
        "switchgear",
        "protection relays",
        "transformer"
    ],

    "Electrical Design Engineer": [
        "electrical design",
        "autocad",
        "autocad electrical",
        "single line diagram",
        "wiring"
    ],

    "Automation Engineer": [
        "plc",
        "scada",
        "automation",
        "control systems",
        "industrial automation"
    ],

    "Mechanical Design Engineer": [
        "autocad",
        "solidworks",
        "catia",
        "cad",
        "mechanical design"
    ],

    "Civil Engineer": [
        "autocad",
        "construction",
        "structural",
        "civil engineering"
    ],

    "Business Analyst": [
        "excel",
        "sql",
        "power bi",
        "business analysis",
        "communication"
    ]
})


# ============================================================
# SESSION STATE
# ============================================================

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_name" not in st.session_state:
    st.session_state.resume_name = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize(text):

    return " ".join(
        str(text).lower().split()
    )


def score_role(resume_text, role):

    resume = normalize(resume_text)

    keywords = ROLE_KEYWORDS.get(
        role,
        []
    )

    if not keywords:
        return 0, [], []

    matched = []
    missing = []

    for keyword in keywords:

        if keyword.lower() in resume:

            matched.append(keyword)

        else:

            missing.append(keyword)

    score = round(
        (
            len(matched)
            /
            len(keywords)
        )
        * 100
    )

    if role.lower() in resume:

        score = min(
            100,
            score + 8
        )

    return (
        score,
        matched,
        missing
    )


def recommend_roles(
    resume_text,
    domain
):

    candidates = []

    if domain == "All Domains":

        roles = []

        for data in CAREER_DATA.values():

            roles.extend(
                data["roles"]
            )

    else:

        roles = CAREER_DATA[
            domain
        ]["roles"]

    seen = set()

    for role in roles:

        if role in seen:
            continue

        seen.add(role)

        score, matched, missing = score_role(
            resume_text,
            role
        )

        candidates.append(
            {
                "role": role,
                "score": score,
                "matched": matched,
                "missing": missing
            }
        )

    candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return candidates[:10]


def get_readiness(score):

    if score >= 80:
        return "Excellent match", "🔥"

    if score >= 65:
        return "Strong potential", "🚀"

    if score >= 50:
        return "Moderate match", "👍"

    return "Needs improvement", "📈"


# ============================================================
# RESUME ANALYSIS PDF
# ============================================================

def create_resume_analysis_pdf(
    results,
    resume_name,
    job_description
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=24,
        leading=28,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        textColor=colors.grey
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=18,
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["Normal"],
        fontSize=10,
        leading=14
    )

    story = []

    story.append(
        Paragraph(
            "RESUMATE",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Resume & Career Intelligence Platform",
            subtitle_style
        )
    )

    story.append(
        Spacer(1, 18)
    )

    story.append(
        Paragraph(
            "RESUME ANALYSIS REPORT",
            heading_style
        )
    )

    info = [
        [
            "Resume",
            resume_name or "Uploaded Resume"
        ],
        [
            "Generated",
            datetime.now().strftime(
                "%d %b %Y, %I:%M %p"
            )
        ]
    ]

    info_table = Table(
        info,
        colWidths=[130, 350]
    )

    info_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#EAF2F8")
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )

    story.append(info_table)

    story.append(
        Spacer(1, 18)
    )

    # ATS SCORE

    ats_score = results.get(
        "ats_score",
        0
    )

    story.append(
        Paragraph(
            "ATS SCORE",
            heading_style
        )
    )

    if ats_score >= 80:
        rating = "EXCELLENT"
    elif ats_score >= 70:
        rating = "STRONG"
    elif ats_score >= 60:
        rating = "MODERATE"
    else:
        rating = "NEEDS IMPROVEMENT"

    ats_table = Table(
        [
            [
                Paragraph(
                    f"<b>{ats_score}/100</b>",
                    ParagraphStyle(
                        "BigScore",
                        parent=normal_style,
                        fontSize=25,
                        alignment=TA_CENTER
                    )
                ),
                Paragraph(
                    f"<b>{rating}</b><br/>ATS Compatibility",
                    ParagraphStyle(
                        "Rating",
                        parent=normal_style,
                        fontSize=13,
                        alignment=TA_CENTER
                    )
                )
            ]
        ],
        colWidths=[240, 240]
    )

    ats_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#F4F6F7")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                colors.HexColor("#5D6D7E")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                14
            )
        ])
    )

    story.append(ats_table)

    story.append(
        Spacer(1, 18)
    )

    # SCORE BREAKDOWN

    story.append(
        Paragraph(
            "SCORE BREAKDOWN",
            heading_style
        )
    )

    score_data = [
        ["Metric", "Score"],
        [
            "Skills Match",
            f"{results.get('skill_score', 0)}%"
        ],
        [
            "Keyword Match",
            f"{results.get('keyword_score', 0)}%"
        ],
        [
            "Completeness",
            f"{results.get('completeness_score', 0)}%"
        ],
        [
            "Resume Quality",
            f"{results.get('quality_score', 0)}%"
        ]
    ]

    score_table = Table(
        score_data,
        colWidths=[300, 180]
    )

    score_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#2C3E50")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "CENTER"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )

    story.append(score_table)

    # MATCHING SKILLS

    story.append(
        Paragraph(
            "MATCHING SKILLS",
            heading_style
        )
    )

    matching = results.get(
        "matching_skills",
        []
    )

    if matching:

        for skill in matching:

            story.append(
                Paragraph(
                    f"✓ {skill.title()}",
                    normal_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No matching skills detected.",
                normal_style
            )
        )

    # MISSING SKILLS

    story.append(
        Paragraph(
            "MISSING SKILLS",
            heading_style
        )
    )

    missing = results.get(
        "missing_skills",
        []
    )

    if missing:

        for skill in missing:

            story.append(
                Paragraph(
                    f"✗ {skill.title()}",
                    normal_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No major missing skills detected.",
                normal_style
            )
        )

    # STRENGTHS

    story.append(
        Paragraph(
            "RESUME STRENGTHS",
            heading_style
        )
    )

    strengths = []

    if results.get("skill_score", 0) >= 70:

        strengths.append(
            "Strong technical skill alignment."
        )

    if results.get("keyword_score", 0) >= 70:

        strengths.append(
            "Good keyword coverage."
        )

    if results.get("completeness_score", 0) >= 80:

        strengths.append(
            "Most important resume sections are present."
        )

    if results.get("quality_score", 0) >= 80:

        strengths.append(
            "Resume contains a healthy amount of content."
        )

    if matching:

        strengths.append(
            f"{len(matching)} relevant skills were detected."
        )

    if not strengths:

        strengths.append(
            "The resume provides a foundation for improvement."
        )

    for item in strengths:

        story.append(
            Paragraph(
                f"✓ {item}",
                normal_style
            )
        )

    # IMPROVEMENTS

    story.append(
        Paragraph(
            "AREAS TO IMPROVE",
            heading_style
        )
    )

    improvements = []

    if results.get("skill_score", 0) < 70:

        improvements.append(
            "Improve technical skill alignment."
        )

    if results.get("keyword_score", 0) < 70:

        improvements.append(
            "Add relevant job-description keywords naturally."
        )

    if results.get("completeness_score", 0) < 80:

        improvements.append(
            "Improve resume section completeness."
        )

    if results.get("quality_score", 0) < 80:

        improvements.append(
            "Add stronger project descriptions and measurable achievements."
        )

    for skill in missing[:8]:

        improvements.append(
            f"Develop or demonstrate experience with {skill.title()}."
        )

    if not improvements:

        improvements.append(
            "Continue tailoring your resume for each job."
        )

    for item in improvements:

        story.append(
            Paragraph(
                f"• {item}",
                normal_style
            )
        )

    # ACTION PLAN

    story.append(
        Paragraph(
            "PERSONALIZED ACTION PLAN",
            heading_style
        )
    )

    actions = [
        "Tailor your resume to each job description.",
        "Use measurable achievements.",
        "Strengthen project descriptions.",
        "Keep technical skills relevant.",
        "Add genuine missing skills after developing them.",
        "Keep LinkedIn and GitHub updated.",
        "Prepare for technical and HR interviews."
    ]

    for number, action in enumerate(
        actions,
        1
    ):

        story.append(
            Paragraph(
                f"{number}. {action}",
                normal_style
            )
        )

    # JD

    if job_description.strip():

        story.append(
            PageBreak()
        )

        story.append(
            Paragraph(
                "TARGET JOB DESCRIPTION",
                heading_style
            )
        )

        safe_jd = (
            job_description
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br/>")
        )

        story.append(
            Paragraph(
                safe_jd,
                normal_style
            )
        )

    story.append(
        Spacer(1, 25)
    )

    story.append(
        Paragraph(
            "Generated by RESUMATE",
            ParagraphStyle(
                "Footer",
                parent=normal_style,
                alignment=TA_CENTER,
                textColor=colors.grey
            )
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# JOB RECOMMENDATION PDF
# ============================================================

def create_job_recommendation_pdf(
    results,
    domain,
    resume_name
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "JobTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=24
    )

    story = []

    story.append(
        Paragraph(
            "RESUMATE",
            title_style
        )
    )

    story.append(
        Paragraph(
            "JOB RECOMMENDATION REPORT",
            styles["Heading1"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            f"<b>Resume:</b> {resume_name}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Career Domain:</b> {domain}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 18)
    )

    story.append(
        Paragraph(
            "TOP RECOMMENDED ROLES",
            styles["Heading2"]
        )
    )

    rows = [
        [
            "Rank",
            "Role",
            "Match"
        ]
    ]

    for index, item in enumerate(
        results,
        1
    ):

        rows.append(
            [
                str(index),
                item["role"],
                f"{item['score']}%"
            ]
        )

    table = Table(
        rows,
        colWidths=[
            60,
            330,
            80
        ]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#243B53")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    story.append(table)

    story.append(
        Spacer(1, 20)
    )

    if results:

        best = results[0]

        story.append(
            Paragraph(
                f"BEST MATCH: {best['role']} — {best['score']}%",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                "<b>Matching skills:</b> "
                + (
                    ", ".join(best["matched"])
                    if best["matched"]
                    else "None detected"
                ),
                styles["Normal"]
            )
        )

        story.append(
            Spacer(1, 8)
        )

        story.append(
            Paragraph(
                "<b>Skills to develop:</b> "
                + (
                    ", ".join(best["missing"])
                    if best["missing"]
                    else "No major gaps"
                ),
                styles["Normal"]
            )
        )

    story.append(
        Spacer(1, 25)
    )

    story.append(
        Paragraph(
            "RESUMATE recommendation scores are guidance "
            "based on resume keyword and skill matching. "
            "They do not guarantee employment.",
            styles["Normal"]
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🚀 RESUMATE"
    )

    st.caption(
        "Resume & Career Intelligence"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "📄 Resume Analyzer",
            "🎯 Job Matcher",
            "📊 Career Dashboard",
            "🤖 Job Recommendations",
            "💡 Recommendations",
            "ℹ️ About"
        ]
    )

    st.divider()

    if st.session_state.resume_name:

        st.success(
            f"Resume loaded:\n{st.session_state.resume_name}"
        )

    else:

        st.info(
            "Upload a resume in Resume Analyzer."
        )


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.markdown(
        "# 🚀 RESUMATE"
    )

    st.subheader(
        "Resume & Career Intelligence Platform"
    )

    st.write(
        "Analyze your resume, match it with jobs, "
        "discover suitable career roles and identify "
        "the skills you need to develop."
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Career Domains",
            len(CAREER_DATA)
        )

    with c2:
        st.metric(
            "Job Roles",
            len(ROLE_KEYWORDS)
        )

    with c3:
        st.metric(
            "Reports",
            "2"
        )

    st.divider()

    st.subheader(
        "✨ Platform Features"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.info(
            """
            ### 📄 Resume Analyzer

            • ATS Score  
            • Skills Match  
            • Keyword Match  
            • Missing Skills  
            • Resume Quality  
            • PDF Report
            """
        )

    with c2:

        st.info(
            """
            ### 🤖 Job Recommendations

            • Multiple Domains  
            • 50+ Roles  
            • Role Match Score  
            • Skill Gaps  
            • Career Suggestions  
            • PDF Report
            """
        )

    with c3:

        st.info(
            """
            ### 📊 Career Dashboard

            • ATS Performance  
            • Career Readiness  
            • Analysis History  
            • Resume Progress
            """
        )


# ============================================================
# RESUME ANALYZER
# ============================================================

elif page == "📄 Resume Analyzer":

    st.title(
        "📄 Resume Analyzer"
    )

    st.write(
        "Upload your resume and compare it against a job description."
    )

    resume = st.file_uploader(
        "Upload your resume",
        type=[
            "pdf",
            "docx"
        ]
    )

    if resume:

        try:

            resume_text = extract_text_from_resume(
                resume
            )

            if resume_text.strip():

                st.session_state.resume_text = (
                    resume_text
                )

                st.session_state.resume_name = (
                    resume.name
                )

                st.success(
                    "✅ Resume uploaded successfully."
                )

            else:

                st.error(
                    "❌ Could not extract text."
                )

        except Exception as error:

            st.error(
                f"❌ Resume extraction error: {error}"
            )

    job_description = st.text_area(
        "Paste Job Description",
        value=st.session_state.job_description,
        height=250,
        placeholder="Paste the complete job description here..."
    )

    st.session_state.job_description = (
        job_description
    )

    if st.button(
        "🔍 Analyze Resume",
        type="primary",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning(
                "⚠️ Please upload your resume."
            )

        elif not job_description.strip():

            st.warning(
                "⚠️ Please paste the job description."
            )

        else:

            try:

                result = analyze_resume(
                    st.session_state.resume_text,
                    job_description
                )

                st.session_state.analysis = result

                st.session_state.history.append(
                    {
                        "date": datetime.now().strftime(
                            "%d %b %Y %H:%M"
                        ),
                        "score": result["ats_score"]
                    }
                )

                st.success(
                    "✅ Resume analyzed successfully!"
                )

            except Exception as error:

                st.error(
                    f"❌ Analysis error: {error}"
                )

    # --------------------------------------------------------
    # ANALYSIS RESULTS
    # --------------------------------------------------------

    results = st.session_state.analysis

    if results:

        st.divider()

        st.subheader(
            "📊 ATS Score"
        )

        ats_score = results["ats_score"]

        st.metric(
            "ATS Score",
            f"{ats_score} / 100"
        )

        st.progress(
            min(
                max(
                    ats_score,
                    0
                ),
                100
            ) / 100
        )

        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Skills Match",
                f"{results['skill_score']}%"
            )

        with c2:

            st.metric(
                "Keyword Match",
                f"{results['keyword_score']}%"
            )

        with c3:

            st.metric(
                "Completeness",
                f"{results.get('completeness_score', 0)}%"
            )

        with c4:

            st.metric(
                "Resume Quality",
                f"{results['quality_score']}%"
            )

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            st.subheader(
                "✅ Matching Skills"
            )

            if results["matching_skills"]:

                for skill in results["matching_skills"]:

                    st.write(
                        f"✓ {skill.title()}"
                    )

            else:

                st.write(
                    "No matching skills found."
                )

        with c2:

            st.subheader(
                "❌ Missing Skills"
            )

            if results["missing_skills"]:

                for skill in results["missing_skills"]:

                    st.write(
                        f"✗ {skill.title()}"
                    )

            else:

                st.write(
                    "No major missing skills detected."
                )

        # ----------------------------------------------------
        # RESTORED RESUME ANALYSIS REPORT
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "📥 Resume Analysis Report"
        )

        st.write(
            "Download your complete ATS analysis as a professional PDF."
        )

        try:

            resume_pdf = create_resume_analysis_pdf(
                results=results,
                resume_name=st.session_state.resume_name,
                job_description=st.session_state.job_description
            )

            st.download_button(
                label="📥 Download Resume Analysis Report",
                data=resume_pdf,
                file_name="RESUMATE_Resume_Analysis_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as error:

            st.error(
                f"❌ Could not create resume report: {error}"
            )


# ============================================================
# JOB MATCHER
# ============================================================

elif page == "🎯 Job Matcher":

    st.title(
        "🎯 Universal Job Matcher"
    )

    if not st.session_state.resume_text:

        st.warning(
            "Please upload your resume first."
        )

    else:

        domain = st.selectbox(
            "Select Career Domain",
            [
                "All Domains"
            ] + list(
                CAREER_DATA.keys()
            )
        )

        if domain == "All Domains":

            roles = sorted(
                ROLE_KEYWORDS.keys()
            )

        else:

            roles = CAREER_DATA[
                domain
            ]["roles"]

        role = st.selectbox(
            "Select Target Role",
            roles
        )

        score, matched, missing = score_role(
            st.session_state.resume_text,
            role
        )

        st.divider()

        st.metric(
            "Job Match Score",
            f"{score}%"
        )

        st.progress(
            score / 100
        )

        readiness, icon = get_readiness(
            score
        )

        st.info(
            f"{icon} {readiness}"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.subheader(
                "✅ Matching"
            )

            for item in matched:

                st.write(
                    f"✓ {item.title()}"
                )

        with c2:

            st.subheader(
                "❌ Missing"
            )

            for item in missing:

                st.write(
                    f"✗ {item.title()}"
                )


# ============================================================
# CAREER DASHBOARD
# ============================================================

elif page == "📊 Career Dashboard":

    st.title(
        "📊 Career Dashboard"
    )

    if not st.session_state.analysis:

        st.info(
            "Analyze your resume first."
        )

    else:

        results = st.session_state.analysis

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "ATS",
                f"{results['ats_score']}/100"
            )

        with c2:

            st.metric(
                "Skills",
                f"{results['skill_score']}%"
            )

        with c3:

            st.metric(
                "Keywords",
                f"{results['keyword_score']}%"
            )

        with c4:

            st.metric(
                "Quality",
                f"{results['quality_score']}%"
            )

        st.divider()

        st.subheader(
            "🚀 Career Readiness"
        )

        st.progress(
            results["ats_score"] / 100
        )

        if results["ats_score"] >= 80:

            st.success(
                "Excellent career readiness!"
            )

        elif results["ats_score"] >= 60:

            st.info(
                "Good progress. Keep improving."
            )

        else:

            st.warning(
                "More resume optimization is recommended."
            )

        if st.session_state.history:

            st.divider()

            st.subheader(
                "📈 Analysis History"
            )

            for item in reversed(
                st.session_state.history
            ):

                st.write(
                    f"**{item['date']}** — "
                    f"ATS Score: {item['score']}/100"
                )


# ============================================================
# JOB RECOMMENDATIONS
# ============================================================

elif page == "🤖 Job Recommendations":

    st.title(
        "🤖 Job Recommendation Engine"
    )

    st.write(
        "Find roles that match your resume across "
        "different branches and industries."
    )

    if not st.session_state.resume_text:

        st.warning(
            "⚠️ Upload your resume first from Resume Analyzer."
        )

    else:

        domain = st.selectbox(
            "Choose Career Domain",
            [
                "All Domains"
            ] + list(
                CAREER_DATA.keys()
            )
        )

        results = recommend_roles(
            st.session_state.resume_text,
            domain
        )

        st.divider()

        st.subheader(
            "🎯 Recommended Roles For You"
        )

        if results:

            best = results[0]

            st.success(
                f"🏆 Best Match: "
                f"{best['role']} — "
                f"{best['score']}%"
            )

            st.divider()

            for index, item in enumerate(
                results,
                1
            ):

                score = item["score"]

                readiness, icon = get_readiness(
                    score
                )

                with st.container(
                    border=True
                ):

                    c1, c2, c3 = st.columns(
                        [4, 2, 1]
                    )

                    with c1:

                        st.markdown(
                            f"### {index}. {item['role']}"
                        )

                        st.caption(
                            f"{icon} {readiness}"
                        )

                    with c2:

                        st.metric(
                            "Match",
                            f"{score}%"
                        )

                        st.progress(
                            score / 100
                        )

                    with c3:

                        st.write(
                            f"Matched: "
                            f"**{len(item['matched'])}**"
                        )

                        st.write(
                            f"Gaps: "
                            f"**{len(item['missing'])}**"
                        )

                    if item["matched"]:

                        st.write(
                            "**Matching:** "
                            + ", ".join(
                                x.title()
                                for x in item["matched"]
                            )
                        )

                    if item["missing"]:

                        st.write(
                            "**Develop:** "
                            + ", ".join(
                                x.title()
                                for x in item["missing"][:6]
                            )
                        )

            # ------------------------------------------------
            # JOB RECOMMENDATION REPORT
            # ------------------------------------------------

            st.divider()

            st.subheader(
                "📥 Job Recommendation Report"
            )

            try:

                job_pdf = create_job_recommendation_pdf(
                    results=results,
                    domain=domain,
                    resume_name=st.session_state.resume_name
                )

                st.download_button(
                    label="📥 Download Job Recommendation Report",
                    data=job_pdf,
                    file_name="RESUMATE_Job_Recommendation_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            except Exception as error:

                st.error(
                    f"❌ Could not create job report: {error}"
                )


# ============================================================
# RECOMMENDATIONS
# ============================================================

elif page == "💡 Recommendations":

    st.title(
        "💡 Personalized Recommendations"
    )

    if not st.session_state.analysis:

        st.info(
            "Analyze your resume first."
        )

    else:

        results = st.session_state.analysis

        st.subheader(
            "🛠️ Areas To Improve"
        )

        missing = results.get(
            "missing_skills",
            []
        )

        if missing:

            for skill in missing:

                st.write(
                    f"📌 {skill.title()}"
                )

        else:

            st.success(
                "No major missing skills detected."
            )

        st.divider()

        st.subheader(
            "🚀 Career Improvement Plan"
        )

        recommendations = [

            "Tailor your resume to every job description.",

            "Use measurable achievements in your experience and projects.",

            "Strengthen technical project descriptions.",

            "Keep your skills section aligned with target roles.",

            "Maintain an updated GitHub profile.",

            "Maintain an updated LinkedIn profile.",

            "Practice technical and HR interviews."

        ]

        for item in recommendations:

            st.write(
                f"✓ {item}"
            )


# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.title(
        "ℹ️ About RESUMATE"
    )

    st.markdown(
        """
        # 🚀 RESUMATE

        **Resume & Career Intelligence Platform**

        RESUMATE helps students and job seekers:

        ✓ Analyze resumes against job descriptions  
        ✓ Calculate ATS-style scores  
        ✓ Identify matching skills  
        ✓ Identify missing skills  
        ✓ Discover suitable career roles  
        ✓ Compare resumes across multiple domains  
        ✓ Track career readiness  
        ✓ Generate professional PDF reports  

        ## 🌎 Supported Domains

        - Computer Science & IT
        - Electronics & Communication
        - Electrical & Electronics
        - Mechanical Engineering
        - Civil Engineering
        - Chemical Engineering
        - Aerospace Engineering
        - Biotechnology
        - Information Science
        - AI & Machine Learning
        - Management & Business
        - Data & Analytics

        ## 📥 Reports

        RESUMATE provides two downloadable reports:

        **1. Resume Analysis Report**

        ATS score, score breakdown, matching skills,
        missing skills, strengths and improvement plan.

        **2. Job Recommendation Report**

        Recommended career roles, match percentages,
        matching skills and skill gaps.

        ### ⚠️ Disclaimer

        RESUMATE provides career guidance based on
        resume content and keyword matching.

        It does not guarantee employment or hiring outcomes.
        """
    )

    st.divider()

    st.caption(
        "RESUMATE — Resume & Career Intelligence Platform"
    )