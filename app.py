import streamlit as st
import json
from datetime import datetime

# ---------------- REQUIRED VARIABLE TYPES ----------------
version_float: float   = 1.1                        # float
allowed_ext: set       = {".json", ".csv", ".txt"}  # set
used_files: set        = set()                      # set
student_record: dict   = {}                         # dict
valid_chars: frozenset = frozenset("-' ")            # frozenset
score_range: range     = range(0, 81)               # range
is_submitted: bool     = False                      # bool
max_score: int         = 80                         # int
app_title: str         = "Breathing & Anxiety Self-Assessment"  # str
state_labels: list     = []                         # list
score_band: tuple      = (0, 80)                    # tuple

# ---------------- QUESTIONS (20 original) ----------------
questions = [
    {"q": "How often do you feel tense or on edge during the day?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How easily do you become calm after a stressful event?",
     "opts": [("Very easily",0),("Fairly easily",1),("With some effort",2),("With great difficulty",3),("I cannot calm down",4)]},
    {"q": "How often do your hands or body feel shaky or trembling?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How frequently do you notice your heart beating fast without physical exertion?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How often do you feel a sense of panic or dread for no clear reason?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How well are you able to concentrate on your studies or daily tasks?",
     "opts": [("Very well",0),("Fairly well",1),("Somewhat",2),("Poorly",3),("Not at all",4)]},
    {"q": "How often do you practise any form of relaxation or breathing exercise?",
     "opts": [("Daily",0),("Several times a week",1),("Once a week",2),("Rarely",3),("Never",4)]},
    {"q": "How frequently do you feel overwhelmed by your academic responsibilities?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How often do you experience difficulty falling or staying asleep due to worry?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How would you describe your general mood throughout the day?",
     "opts": [("Very positive",0),("Mostly positive",1),("Neutral",2),("Mostly negative",3),("Very negative",4)]},
    {"q": "How often do you feel short of breath or notice irregular breathing during rest?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How confident do you feel in managing stressful academic situations?",
     "opts": [("Very confident",0),("Fairly confident",1),("Somewhat confident",2),("Rarely confident",3),("Not confident at all",4)]},
    {"q": "How often do physical symptoms such as headaches or stomach discomfort accompany your stress?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How frequently do you avoid social interactions because of anxiety or low energy?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How often do you feel that your worries are difficult to control?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How would you rate the quality of your breathing during a stressful moment?",
     "opts": [("Very controlled",0),("Mostly controlled",1),("Slightly irregular",2),("Notably irregular",3),("Severely disrupted",4)]},
    {"q": "How often do you feel fatigued or drained even without significant physical activity?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How frequently do you use breathing techniques or mindfulness to manage anxiety?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": "How often do you feel that academic pressure negatively affects your mental health?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How optimistic do you feel about your ability to cope with upcoming challenges?",
     "opts": [("Very optimistic",0),("Mostly optimistic",1),("Neutral",2),("Mostly pessimistic",3),("Very pessimistic",4)]},
]

# Populate state_labels list
state_labels = ["No Anxiety", "Mild Anxiety", "Moderate Anxiety",
                "High Anxiety", "Severe Anxiety", "Critical Anxiety"]

# ---------------- PSYCHOLOGICAL STATES ----------------
psych_states = {
    "No Anxiety":       (0,  14),
    "Mild Anxiety":     (15, 29),
    "Moderate Anxiety": (30, 44),
    "High Anxiety":     (45, 59),
    "Severe Anxiety":   (60, 74),
    "Critical Anxiety": (75, 80),
}

STATE_DESCRIPTIONS = {
    "No Anxiety":       "Calm and well-regulated emotional state. No intervention needed.",
    "Mild Anxiety":     "Occasional tension present. Self-care and relaxation practices are advisable.",
    "Moderate Anxiety": "Noticeable anxiety affecting daily functioning. Breathing exercises are recommended.",
    "High Anxiety":     "Persistent anxiety detected. Seeking guidance from a counsellor is advisable.",
    "Severe Anxiety":   "Significant distress. Professional psychological support is strongly recommended.",
    "Critical Anxiety": "Acute psychological distress. Immediate professional or medical assistance required.",
}

STATE_COLOURS = {
    "No Anxiety":       "#27ae60",
    "Mild Anxiety":     "#2ecc71",
    "Moderate Anxiety": "#f39c12",
    "High Anxiety":     "#e67e22",
    "Severe Anxiety":   "#e74c3c",
    "Critical Anxiety": "#8e44ad",
}

# ---------------- VALIDATION FUNCTIONS ----------------

def validate_name(name: str) -> bool:
    """
    Validates name using a for-loop to check each character.
    Allows letters, hyphens, apostrophes, and spaces only.
    Covers: O'Connor, Smith-Jones, Mary Ann.
    """
    name = name.strip()
    if len(name) == 0:
        return False
    for char in name:
        if not (char.isalpha() or char in valid_chars):
            return False
    return True


def validate_dob(dob: str) -> bool:
    """
    Validates date of birth in DD/MM/YYYY format.
    Checks format, logical values, and that date is not in the future.
    """
    try:
        parsed = datetime.strptime(dob, "%d/%m/%Y")
        if parsed > datetime.now():
            return False
        age_years: int = (datetime.now() - parsed).days // 365
        if age_years > 120:
            return False
        return True
    except ValueError:
        return False


def validate_student_id(sid: str) -> bool:
    """Validates that student ID contains digits only."""
    return sid.isdigit() and len(sid) > 0


def interpret_score(score: int) -> str:
    """Classifies the total score into a psychological state."""
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"


# ---------------- STREAMLIT APP ----------------

st.set_page_config(
    page_title="Breathing & Anxiety Self-Assessment",
    page_icon="🫁",
    layout="centered"
)

st.title("🫁 Breathing & Anxiety Self-Assessment")
st.caption("Westminster International University in Tashkent")
st.info("Please fill in your details and answer all 20 questions honestly. "
        "Reflect on your experience over the **past two weeks**.")

# ---- Session state setup ----
if "page" not in st.session_state:
    st.session_state.page = "details"
if "record" not in st.session_state:
    st.session_state.record = {}
if "answers" not in st.session_state:
    st.session_state.answers = []
if "total_score" not in st.session_state:
    st.session_state.total_score = 0

# ================================================================
# PAGE 1: USER DETAILS
# ================================================================
if st.session_state.page == "details":

    st.subheader("Step 1 — Your Details")

    with st.form("details_form"):
        given_name = st.text_input("Given Name", placeholder="e.g. Mary Ann")
        surname    = st.text_input("Surname",    placeholder="e.g. O'Connor")
        dob        = st.text_input("Date of Birth (DD/MM/YYYY)", placeholder="e.g. 15/03/2004")
        sid        = st.text_input("Student ID (digits only)",   placeholder="e.g. 123456")

        submitted = st.form_submit_button("Start Assessment →")

    if submitted:
        errors = []

        if not validate_name(given_name):
            errors.append("❌ Given name is invalid. Use only letters, hyphens (-), apostrophes ('), or spaces.")
        if not validate_name(surname):
            errors.append("❌ Surname is invalid. Use only letters, hyphens (-), apostrophes ('), or spaces.")
        if not validate_dob(dob):
            errors.append("❌ Date of birth is invalid. Please use DD/MM/YYYY format (e.g. 15/03/2004).")
        if not validate_student_id(sid):
            errors.append("❌ Student ID must contain digits only (e.g. 123456).")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.session_state.record = {
                "name":       given_name.strip(),
                "surname":    surname.strip(),
                "dob":        dob.strip(),
                "student_id": sid.strip(),
                "version":    version_float
            }
            st.session_state.page = "survey"
            st.rerun()

# ================================================================
# PAGE 2: SURVEY QUESTIONS
# ================================================================
elif st.session_state.page == "survey":

    st.subheader("Step 2 — Answer All Questions")
    st.caption("Select one option per question, then click Submit at the bottom.")

    total: int = len(questions)

    with st.form("survey_form"):
        responses = []

        for idx, q in enumerate(questions):
            st.markdown(f"**Q{idx+1} of {total}. {q['q']}**")
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.radio(
                label=f"q{idx}",
                options=opt_labels,
                index=None,
                key=f"q{idx}",
                label_visibility="collapsed"
            )
            responses.append((q, choice))
            st.divider()

        submit_survey = st.form_submit_button("Submit Assessment ✓")

    if submit_survey:
        # Validate all questions answered using a for-loop
        unanswered = []
        for i, (q, choice) in enumerate(responses):
            if choice is None:
                unanswered.append(i + 1)

        if unanswered:
            st.error(f"❌ Please answer all questions. Unanswered: {unanswered}")
        else:
            total_score: int = 0
            answers: list    = []

            for q, choice in responses:
                score: int = next(s for label, s in q["opts"] if label == choice)
                total_score += score
                answers.append({
                    "question":        q["q"],
                    "selected_option": choice,
                    "score":           score
                })

            st.session_state.total_score = total_score
            st.session_state.answers     = answers
            st.session_state.page        = "result"
            st.rerun()

# ================================================================
# PAGE 3: RESULT
# ================================================================
elif st.session_state.page == "result":

    total_score: int  = st.session_state.total_score
    answers: list     = st.session_state.answers
    rec: dict         = st.session_state.record

    result_label: str  = interpret_score(total_score)
    description: str   = STATE_DESCRIPTIONS.get(result_label, "")
    colour: str        = STATE_COLOURS.get(result_label, "#2c3e50")
    score_pct: float   = round((total_score / max_score) * 100, 2)
    completed_at: str  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    st.subheader("Step 3 — Your Result")

    # Coloured result banner
    st.markdown(
        f"""
        <div style="background-color:{colour};padding:20px;border-radius:10px;text-align:center;">
            <h2 style="color:white;margin:0;">{result_label}</h2>
            <p style="color:white;margin:4px 0 0 0;font-size:16px;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("")

    col1, col2 = st.columns(2)
    col1.metric("Total Score", f"{total_score} / {max_score}")
    col2.metric("Score Percentage", f"{score_pct}%")

    st.markdown("---")

    # Build the full result record
    full_record: dict = {
        "name":         rec.get("name", ""),
        "surname":      rec.get("surname", ""),
        "dob":          rec.get("dob", ""),
        "student_id":   rec.get("student_id", ""),
        "version":      version_float,
        "total_score":  total_score,
        "max_score":    max_score,
        "score_pct":    score_pct,
        "result":       result_label,
        "description":  description,
        "answers":      answers,
        "completed_at": completed_at
    }

    # Save locally and offer download
    json_filename: str = f"{rec.get('student_id', 'result')}_result.json"
    json_str: str      = json.dumps(full_record, indent=2, ensure_ascii=False)

    st.download_button(
        label="💾  Download Result as JSON",
        data=json_str,
        file_name=json_filename,
        mime="application/json"
    )

    # Show full answers in expander
    with st.expander("📋 View Full Answers"):
        for i, ans in enumerate(answers, 1):
            st.markdown(f"**Q{i}. {ans['question']}**")
            st.markdown(f"&nbsp;&nbsp;&nbsp;Answer: *{ans['selected_option']}* — score: `{ans['score']}`")
            st.divider()

    if st.button("⟵ Start New Assessment"):
        for key in ["page", "record", "answers", "total_score"]:
            del st.session_state[key]
        st.rerun()
