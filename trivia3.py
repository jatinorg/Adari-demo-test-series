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
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

# Quiz configuration
TOTAL_TIME_LIMIT = 420   # 7 minutes
WARNING_THRESHOLDS = {
    'critical': 60,      # Red blinking - 1 minute
    'warning': 120,      # Red - 2 minutes
    'caution': 180      # Orange - 3 minutes
}

# Questions with solutions
questions = [
    {
        "question": """Directions: Study the following digit-letter-symbol sequence carefully:
        C%B K 1 & A W 5 P E 4 Q @ 7 F 6 G © Z J L 2 € D ¥ M #8
        
        How many such symbols are there in the above sequence, each of which is immediately preceded by a consonant and immediately followed by a number?""",
        "options": ["None", "One", "Two", "Four", "None of these"],
        "correct_answer": "Two",
        "solution": "Solution: Q@7 and M#8 are the two instances where a symbol is preceded by a consonant and followed by a number."
    },
    {
        "question": """Using the same sequence:
        C%B K 1 & A W 5 P E 4 Q @ 7 F 6 G © Z J L 2 € D ¥ M #8
        
        Which of the following is fifth to the left of 15th element from the left?""",
        "options": ["S", "P", "E", "#", "None of these"],
        "correct_answer": "P",
        "solution": "Solution: Count 15 elements from left, then count 5 more to the left to find 'P'."
    },
    {
        "question": """Using the same sequence:
        C%B K 1 & A W 5 P E 4 Q @ 7 F 6 G © Z J L 2 € D ¥ M #8
        
        If all the numbers are dropped in the given series, then which element will be at sixth position from right end?""",
        "options": ["Z", "M", "L", "D", "None of these"],
        "correct_answer": "L",
        "solution": "Solution: After removing numbers and counting from right end: M, D, ¥, €, J, L"
    },
    {
        "question": """Using the same sequence:
        C%B K 1 & A W 5 P E 4 Q @ 7 F 6 G © Z J L 2 € D ¥ M #8
        
        How many such numbers are there in the above sequence, each of which is immediately preceded by a vowel and immediately followed by a consonant?""",
        "options": ["Three", "Two", "None", "One", "None of these"],
        "correct_answer": "One",
        "solution": "Solution: Only E4Q satisfies the condition where '4' is preceded by vowel 'E' and followed by consonant 'Q'."
    },
    {
        "question": """Using the same sequence:
        C%B K 1 & A W 5 P E 4 Q @ 7 F 6 G © Z J L 2 € D ¥ M #8
        
        What should come in place of question mark in the following on the basis of above sequence?
        B, &, P, 7, ?""",
        "options": ["#", "M", "D", "2", "J"],
        "correct_answer": "J",
        "solution": "Solution: The pattern follows elements at regular intervals in the sequence B → & → P → 7 → J"
    }
]

def format_time(seconds):
    """Format seconds into minutes:seconds"""
    if seconds is None:
        return "00:00"
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_timer_style(remaining_time):
    """Return timer style based on remaining time"""
    if remaining_time <= WARNING_THRESHOLDS['critical']:
        return "red", True  # Color, Should blink
    elif remaining_time <= WARNING_THRESHOLDS['warning']:
        return "red", False
    elif remaining_time <= WARNING_THRESHOLDS['caution']:
        return "orange", False
    return "green", False

def display_timer(remaining_time):
    """Display a prominent timer with appropriate styling"""
    color, should_blink = get_timer_style(remaining_time)
    
    # Warning messages based on time
    warning_message = ""
    if remaining_time <= WARNING_THRESHOLDS['critical']:
        warning_message = "⚠️ HURRY UP! Less than 1 minute remaining!"
    elif remaining_time <= WARNING_THRESHOLDS['warning']:
        warning_message = "⚠️ 2 minutes remaining!"
    elif remaining_time <= WARNING_THRESHOLDS['caution']:
        warning_message = "⚠️ 3 minutes remaining!"

    timer_html = f"""
        <div style='text-align: center; margin: 10px 0;'>
            <div style='
                font-size: 2.5rem;
                font-weight: bold;
                color: {color};
                {"animation: blink 1s linear infinite" if should_blink else ""};
                padding: 10px;
                border: 2px solid {color};
                border-radius: 10px;
                display: inline-block;
            '>
                ⏱️ {format_time(remaining_time)}
            </div>
            <div style='color: {color}; font-weight: bold; margin-top: 5px;'>
                {warning_message}
            </div>
        </div>
    """
    st.markdown(timer_html, unsafe_allow_html=True)

def display_solutions():
    """Display solutions with detailed explanations"""
    st.markdown("### 📝 Review Solutions")
    
    for i, question in enumerate(questions):
        with st.expander(f"Question {i + 1}"):
            st.markdown(f"**Question:**\n{question['question']}")
            st.markdown("**Options:**")
            for option in question['options']:
                prefix = "✅" if option == question['correct_answer'] else "❌"
                highlight = "background-color: #90EE90;" if option == question['correct_answer'] else ""
                selected = "👉 " if st.session_state.user_answers.get(i) == option else ""
                st.markdown(f"""
                    <div style='{highlight} padding: 5px; border-radius: 5px;'>
                        {prefix} {selected} {option}
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"**Your Answer:** {st.session_state.user_answers.get(i, 'Not answered')}")
            st.markdown(f"**Correct Answer:** {question['correct_answer']}")
            st.markdown(f"**{question['solution']}**")
            
            # Show if answer was correct and marks awarded
            if i in st.session_state.user_answers:
                if st.session_state.user_answers[i] == question['correct_answer']:
                    st.markdown("✅ **+2 marks awarded**")
                else:
                    st.markdown("❌ **-0.5 marks deducted**")
            else:
                st.markdown("❌ **No answer submitted**")

def main():
    # Page configuration and CSS remain the same...
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
            background-color: #f0f2f6;
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
    
    # Previous code for user registration and quiz start remains the same...
    
    # Quiz section
    if st.session_state.quiz_started and not st.session_state.quiz_complete:
        # Update and display timer
        current_time = time.time()
        time_elapsed = current_time - st.session_state.question_start_time
        st.session_state.remaining_time = max(0, TOTAL_TIME_LIMIT - time_elapsed)
        
        display_timer(st.session_state.remaining_time)
        
        # Rest of the quiz logic remains the same, but store user answers
        current_q = questions[st.session_state.current_question]
        answer = st.radio("Select your answer:", current_q["options"], key=f"q_{st.session_state.current_question}")
        st.session_state.user_answers[st.session_state.current_question] = answer
        
        # Auto-submit logic and buttons remain the same...
        if st.session_state.remaining_time <= 0:
            submit_quiz()
            st.experimental_rerun()
        
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
                st.experimental_rerun()
        
        # Submit entire quiz button
        if st.button("Submit Quiz"):
            submit_quiz()
            st.experimental_rerun()

    # Display results and solutions if quiz is complete
    if st.session_state.quiz_complete:
        st.success("Assessment Complete! 🎉")
        st.markdown(f"<p class='score-display'>Final Score: {st.session_state.score}/{len(questions)*2}</p>", unsafe_allow_html=True)
        
        # Display solutions
        display_solutions()
        
        if st.button("Start New Assessment"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()

    # Display progress bar
    if st.session_state.quiz_started and not st.session_state.quiz_complete:
        progress = (st.session_state.current_question + 1) / len(questions)
        st.progress(progress)

if __name__ == "__main__":
    main()