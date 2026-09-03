import streamlit as st
from groq import Groq


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI ATS Resume Builder",
    page_icon="📄",
    layout="wide"
)


# ==========================================
# GROQ CLIENT
# ==========================================

if "GROQ_API_KEY" not in st.secrets:
    st.error("GROQ_API_KEY is not configured.")
    st.stop()

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

MODEL = "openai/gpt-oss-20b"


# ==========================================
# RESUME GENERATOR
# ==========================================

def build_resume(
    name,
    contact,
    target_job,
    job_description,
    experience,
    skills,
    education,
    projects
):

    prompt = f"""
You are an expert ATS resume writer.

Create an ATS-friendly resume using ONLY the information
provided by the candidate.

IMPORTANT RULES:

- Never invent experience.
- Never invent companies.
- Never invent dates.
- Never invent technologies.
- Never invent achievements.
- Never invent education.
- Never invent certifications.

You MAY rewrite existing information to make it more
professional and achievement-oriented.

Tailor the resume to the target job.

Use keywords from the job description ONLY when the
candidate's information supports those keywords.

Do not keyword stuff.

Do not use tables.

Do not use emojis.

Use standard ATS-friendly section headings.

TARGET JOB:
{target_job}

JOB DESCRIPTION:
{job_description}

CANDIDATE:

NAME:
{name}

CONTACT:
{contact}

WORK EXPERIENCE:
{experience}

SKILLS:
{skills}

EDUCATION:
{education}

PROJECTS:
{projects}

Return the resume in Markdown.

Use this structure:

# NAME

Contact information

## PROFESSIONAL SUMMARY

...

## TECHNICAL SKILLS

...

## PROFESSIONAL EXPERIENCE

...

## PROJECTS

...

## EDUCATION

...

## CERTIFICATIONS

...

At the end include:

## ATS KEYWORD MATCH

List important keywords from the job description
that are supported by the candidate.

## MISSING KEYWORDS

List important job keywords that are not supported
by the candidate information.

## ATS SCORE

Give a realistic score from 0-100.
"""


    response = client.chat.completions.create(
        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert technical recruiter "
                    "and ATS resume writer."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3,

        max_completion_tokens=4000
    )

    return response.choices[0].message.content


# ==========================================
# UI
# ==========================================

st.title("📄 AI ATS Resume Builder")

st.write(
    "Create an ATS-friendly resume tailored to a specific "
    "job description."
)

st.divider()


# ==========================================
# PERSONAL INFORMATION
# ==========================================

st.header("👤 Personal Information")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Full Name",
        placeholder="John Doe"
    )

    email = st.text_input(
        "Email",
        placeholder="john@example.com"
    )

    phone = st.text_input(
        "Phone",
        placeholder="+92..."
    )


with col2:

    location = st.text_input(
        "Location",
        placeholder="Pakistan"
    )

    linkedin = st.text_input(
        "LinkedIn",
        placeholder="https://linkedin.com/in/..."
    )

    github = st.text_input(
        "GitHub",
        placeholder="https://github.com/..."
    )


contact = " | ".join(
    x for x in [
        email,
        phone,
        location,
        linkedin,
        github
    ]
    if x
)


# ==========================================
# TARGET JOB
# ==========================================

st.header("🎯 Target Job")

target_job = st.text_input(
    "Job Title",
    placeholder="Senior .NET Developer"
)

job_description = st.text_area(
    "Paste Job Description",
    height=300,
    placeholder="Paste the complete job description here..."
)


# ==========================================
# EXPERIENCE
# ==========================================

st.header("💼 Work Experience")

experience = st.text_area(
    "Your Work Experience",
    height=300,
    placeholder="""Company: ABC Technologies
Position: Software Developer
Dates: 2023 - Present

- Developed REST APIs using ASP.NET Core
- Worked with Angular
- Worked with SQL Server

Company: XYZ
Position: Software Engineer
Dates: 2021 - 2023

- ...
"""
)


# ==========================================
# SKILLS
# ==========================================

st.header("🛠️ Skills")

skills = st.text_area(
    "Technical Skills",
    height=150,
    placeholder=(
        "C#, .NET 8, ASP.NET Core, Angular, "
        "SQL Server, Oracle, Docker, RabbitMQ"
    )
)


# ==========================================
# EDUCATION
# ==========================================

st.header("🎓 Education")

education = st.text_area(
    "Education",
    height=120,
    placeholder="""BS Computer Science
XYZ University
2017 - 2021
CGPA: 3.67/4.00"""
)


# ==========================================
# PROJECTS
# ==========================================

st.header("🚀 Projects")

projects = st.text_area(
    "Projects",
    height=200,
    placeholder="""Learning Management System

Built an LMS using .NET 8 and Angular.

Technologies:
.NET 8, Angular, SQL Server, Docker

Responsibilities:
- Designed REST APIs
- Implemented authentication
- Built Angular frontend
"""
)


# ==========================================
# GENERATE
# ==========================================

st.divider()

generate = st.button(
    "✨ Generate ATS Resume",
    type="primary",
    use_container_width=True
)


# ==========================================
# GENERATION
# ==========================================

if generate:

    if not name.strip():

        st.warning(
            "Please enter your name."
        )

    elif not target_job.strip():

        st.warning(
            "Please enter the target job."
        )

    elif not job_description.strip():

        st.warning(
            "Please paste the job description."
        )

    elif not experience.strip():

        st.warning(
            "Please enter your work experience."
        )

    else:

        with st.spinner(
            "🤖 Creating your ATS-optimized resume..."
        ):

            try:

                resume = build_resume(
                    name=name,
                    contact=contact,
                    target_job=target_job,
                    job_description=job_description,
                    experience=experience,
                    skills=skills,
                    education=education,
                    projects=projects
                )

                st.session_state["resume"] = resume

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )


# ==========================================
# DISPLAY RESULT
# ==========================================

if "resume" in st.session_state:

    st.divider()

    st.header("📄 Your ATS Resume")

    resume = st.session_state["resume"]

    st.markdown(resume)

    st.download_button(
        label="⬇️ Download Resume",
        data=resume,
        file_name="ats_resume.md",
        mime="text/markdown",
        use_container_width=True
    )