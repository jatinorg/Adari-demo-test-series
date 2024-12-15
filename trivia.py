import streamlit as st
import json
import os
from datetime import datetime
import time

# Initialize session state variables
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False
if 'question_start_time' not in st.session_state:
    st.session_state.question_start_time = None
if 'remaining_time' not in st.session_state:
    st.session_state.remaining_time = None

# Quiz configuration
QUESTION_TIME_LIMIT = 45  # seconds per question
TOTAL_TIME_LIMIT = 300   # 5 minutes for entire quiz
TIME_WARNING = 60        # seconds remaining when to show warning
CORRECT_MARKS = 2        # marks for correct answer
WRONG_MARKS = -0.5       # negative marking for wrong answer

# Quiz questions
questions = [
    {
        "question": """Directions: Study the following digit-letter-symbol sequence carefully:
        C%B K 1 & A W 5 P E 4 Q @ 7 F 6 G © Z J L 2 € D ¥ M #8
        
        How many such symbols are there in the above sequence, each of which is immediately preceded by a consonant and immediately followed by a number?""",
        "options": ["None", "One", "Two", "Four", "None of these"],
        "correct_answer": "Two"
    },
    {
        "question": """Using the same sequence:
        C%B K 1 & A W 5 P E 4 Q @ 7 F 6 G © Z J L 2 € D ¥ M #8
        
        Which of the following is fifth to the left of 15th element from the left?""",
        "options": ["S", "P", "E", "#", "None of these"],
        "correct_answer": "P"
    },
    {
        "question": """Using the same sequence:
        C%B K 1 & A W 5 P E 4 Q @ 7 F 6 G © Z J L 2 € D ¥ M #8
        
        If all the numbers are dropped in the given series, then which element will be at sixth position from right end?""",
        "options": ["Z", "M", "L", "D", "None of these"],
        "correct_answer": "L"
    },
    {
        "question": """Using the same sequence:
        C%B K 1 & A W 5 P E 4 Q @ 7 F 6 G © Z J L 2 € D ¥ M #8
        
        How many such numbers are there in the above sequence, each of which is immediately preceded by a vowel and immediately followed by a consonant?""",
        "options": ["Three", "Two", "None", "One", "None of these"],
        "correct_answer": "One"
    },
    {
        "question": """Using the same sequence:
        C%B K 1 & A W 5 P E 4 Q @ 7 F 6 G © Z J L 2 € D ¥ M #8
        
        What should come in place of question mark in the following on the basis of above sequence?
        B, &, P, 7, ?""",
        "options": ["#", "M", "D", "2", "J"],
        "correct_answer": "J"
    }
]

def save_user_data(user_data):
    """Save user data to a JSON file"""
    filename = "user_data.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    
    existing_data.append(user_data)
    
    with open(filename, "w") as f:
        json.dump(existing_data, f, indent=4)

def format_time(seconds):
    """Format seconds into minutes:seconds"""
    if seconds is None:
        return "00:00"
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_timer_color(remaining_time):
    """Return color based on remaining time"""
    if remaining_time <= TIME_WARNING/3:
        return "red"
    elif remaining_time <= TIME_WARNING:
        return "orange"
    return "green"

def submit_quiz():
    """Handle quiz submission"""
    st.session_state.quiz_complete = True
    final_time = TOTAL_TIME_LIMIT - st.session_state.remaining_time
    
    # Save user data
    user_data = {
        "name": st.session_state.user_name,
        "email": st.session_state.user_email,
        "score": st.session_state.score,
        "total_questions": len(questions),
        "completion_time": format_time(final_time),
        "completion_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_user_data(user_data)

def main():
    # Page configuration
    st.set_page_config(page_title="Adari Institute - Aptitude Test", page_icon="🎓", layout="wide")
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .main-title {
            text-align: center;
            color: #1E3D59;
            padding: 20px;
        }
        .timer-warning {
            color: red;
            font-weight: bold;
            animation: blink 1s linear infinite;
        }
        .question-text {
            background-color: #add8e6;
            padding: 20px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .score-display {
            font-size: 20px;
            font-weight: bold;
            color: #1E3D59;
        }
        @keyframes blink {
            50% { opacity: 0; }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title and Header
    st.markdown("<h1 class='main-title'>🎓 Adari Institute</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='main-title'>Aptitude Assessment</h2>", unsafe_allow_html=True)
    
    # User registration/login section
    with st.sidebar:
        st.header("User Details")
        if not st.session_state.quiz_started:
            st.session_state.user_name = st.text_input("Enter your name")
            st.session_state.user_email = st.text_input("Enter your email")
        
        if st.session_state.quiz_started:
            st.markdown("---")
            st.markdown(f"""
            ### Scoring Rules:
            - Correct Answer: +{CORRECT_MARKS} marks
            - Wrong Answer: {WRONG_MARKS} marks
            - Current Score: {st.session_state.score}
            """)

    # Start quiz button
    if not st.session_state.quiz_started and not st.session_state.quiz_complete:
        if st.session_state.user_name and st.session_state.user_email:
            st.info("Important: Read each question carefully. There is negative marking for wrong answers.")
            if st.button("Start Quiz"):
                st.session_state.quiz_started = True
                st.session_state.remaining_time = TOTAL_TIME_LIMIT
                st.session_state.question_start_time = time.time()
                #st.rerun()
        else:
            st.warning("Please enter your details in the sidebar to start the quiz!")
            return

    # Quiz section
    if st.session_state.quiz_started and not st.session_state.quiz_complete:
        # Update timer
        current_time = time.time()
        time_elapsed = current_time - st.session_state.question_start_time
        st.session_state.remaining_time = max(0, TOTAL_TIME_LIMIT - time_elapsed)
        
        # Display timer with color coding
        timer_color = get_timer_color(st.session_state.remaining_time)
        timer_html = f"""
            <div style='text-align: center; color: {timer_color}; 
                {"animation: blink 1s linear infinite" if timer_color == "red" else ""}'>
                <h2>⏱️ Time Remaining: {format_time(st.session_state.remaining_time)}</h2>
            </div>
        """
        st.markdown(timer_html, unsafe_allow_html=True)
        
        # Display current question
        current_q = questions[st.session_state.current_question]
        st.subheader(f"Question {st.session_state.current_question + 1} of {len(questions)}")
        st.markdown(f"<div class='question-text'>{current_q['question']}", unsafe_allow_html=True)
        
        # Answer options
        answer = st.radio("Select your answer:", current_q["options"], key=f"q_{st.session_state.current_question}")
        
        # Submit answer button or auto-submit on time out
        if st.session_state.remaining_time <= 0:
            submit_quiz()
            #st.rerun()
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("Submit Answer"):
                if answer == current_q["correct_answer"]:
                    st.success("Correct! 🎉")
                    st.session_state.score += CORRECT_MARKS
                else:
                    st.error(f"Wrong! The correct answer was {current_q['correct_answer']}")
                    st.session_state.score += WRONG_MARKS
                
                if st.session_state.current_question < len(questions) - 1:
                    st.session_state.current_question += 1
                    st.session_state.question_start_time = time.time()
                else:
                    submit_quiz()
                #st.rerun()
        
        # Submit entire quiz button
        if st.button("Submit Quiz"):
            submit_quiz()
            #st.experimental_rerun()

    # Display results if quiz is complete
    if st.session_state.quiz_complete:
        st.success("Assessment Complete! 🎉")
        st.markdown(f"<p class='score-display'>Final Score: {st.session_state.score}/{len(questions)*CORRECT_MARKS}</p>", unsafe_allow_html=True)
        
        if st.button("Start New Assessment"):
            for key in st.session_state.keys():
                del st.session_state[key]
            #st.rerun()

    # Display progress bar
    if st.session_state.quiz_started and not st.session_state.quiz_complete:
        progress = (st.session_state.current_question + 1) / len(questions)
        st.progress(progress)

if __name__ == "__main__":
    main()