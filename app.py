import streamlit as st
from openai import OpenAI

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="AI Career Navigator", layout="wide")

# OpenRouter client (DeepSeek / Qwen)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

# -----------------------------
# CAREER SCORING FUNCTION
# -----------------------------
def score_careers(responses):
    math = responses["math"]
    tech = responses["tech"]
    people = responses["people"]
    creativity = responses["creativity"]
    business = responses["business"]
    leadership = responses["leadership"]
    research = responses["research"]
    communication = responses["communication"]
    risk = responses["risk"]
    problem_solving = responses["problem_solving"]

    careers = {
        "AI Engineer": (
            math * 0.3 + tech * 0.4 + research * 0.2 + creativity * 0.1
        ),

        "Software Engineer": (
            tech * 0.45 +
            math * 0.35 +
            creativity * 0.10 +
            problem_solving * 0.10
            ),

        "Doctor": (
            people * 0.4 + research * 0.2 + communication * 0.2 + math * 0.2
        ),

        "Entrepreneur": (
            business * 0.3 + leadership * 0.3 + risk * 0.2 + creativity * 0.2
        ),

        "Data Scientist": (
            math * 0.4 + tech * 0.3 + research * 0.2 + communication * 0.1
        ),

        "Designer": (
            creativity * 0.5 + tech * 0.2 + communication * 0.2 + people * 0.1
        ),
    }

    return sorted(careers.items(), key=lambda x: x[1], reverse=True)


# -----------------------------
# AI FUNCTION
# -----------------------------
def generate_ai_report(profile, top_careers):
    prompt = f"""
You are a professional career counselor.

Student Profile:
{profile}

Top Career Matches:
{top_careers}

Give:
1. Personality analysis
2. Why these careers fit
3. Skills to improve
4. Recommended university majors
5. 5-year roadmap
6. AI impact on these careers

Keep it clear and motivating.
"""

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def chat_with_ai(user_input, context):
    prompt = f"""
You are an AI career advisor.

Student Context:
{context}

User Question:
{user_input}

Answer in a helpful, simple way.
"""

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# -----------------------------
# UI LAYOUT
# -----------------------------
st.title("🚀 AI Career Navigator")

col1, col2 = st.columns([1, 1])

# -----------------------------
# SURVEY (LEFT SIDE)
# -----------------------------
with col1:
    st.header("📊 Career Survey (12 Questions)")

    responses = {
        "math": st.slider("Math skills", 1, 5, 3),
        "tech": st.slider("Technology interest", 1, 5, 3),
        "people": st.slider("Helping people", 1, 5, 3),
        "creativity": st.slider("Creativity", 1, 5, 3),
        "business": st.slider("Business interest", 1, 5, 3),
        "leadership": st.slider("Leadership", 1, 5, 3),
        "research": st.slider("Research interest", 1, 5, 3),
        "communication": st.slider("Communication", 1, 5, 3),
        "risk": st.slider("Risk taking", 1, 5, 3),
        "problem_solving": st.slider("Problem Solving", 1, 5, 3)
    }

    if st.button("🎯 Generate Career Results"):

        results = score_careers(responses)
        top3 = results[:3]

        st.session_state["results"] = results
        st.session_state["top3"] = top3
        st.session_state["responses"] = responses

        st.success("Results generated!")

        for i, (career, score) in enumerate(results[:5]):
            st.write(f"{i+1}. {career} — {round(score,2)}")

# -----------------------------
# CHATBOT (RIGHT SIDE)
# -----------------------------
with col2:
    st.header("🤖 AI Career Chat")

    if "responses" in st.session_state:

        context = {
            "survey": st.session_state["responses"],
            "top_careers": st.session_state["top3"]
        }

        user_input = st.text_input("Ask anything about your career...")

        if user_input:
            answer = chat_with_ai(user_input, context)
            st.write(answer)

    else:
        st.info("Complete the survey to unlock personalized AI chat.")


# -----------------------------
# AI REPORT SECTION
# -----------------------------
if "results" in st.session_state:

    st.divider()
    st.header("🧠 AI Career Report")

    profile = st.session_state["responses"]
    top_careers = st.session_state["top3"]

    if st.button("Generate AI Report"):

        report = generate_ai_report(profile, top_careers)
        st.write(report)
