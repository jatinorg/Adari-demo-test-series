import streamlit as st
import json
import os
from datetime import datetime, timedelta
import time

# Initialize session state variables
def initialize_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'test_started' not in st.session_state:
        st.session_state.test_started = False
    if 'test_complete' not in st.session_state:
        st.session_state.test_complete = False
    if 'question_start_time' not in st.session_state:
        st.session_state.question_start_time = None
    if 'remaining_time' not in st.session_state:
        st.session_state.remaining_time = None
    if 'selected_test' not in st.session_state:
        st.session_state.selected_test = None

# Test configuration
QUESTION_TIME_LIMIT = 45  # seconds per question
TOTAL_TIME_LIMIT = 300   # 5 minutes for entire test
TIME_WARNING = 60        # seconds remaining when to show warning
CORRECT_MARKS = 2        # marks for correct answer
WRONG_MARKS = -0.5       # negative marking for wrong answer

# Sample questions (you can load this from a database or file)
questions = [
    {
        "question": """Directions: Study the following digit-letter-symbol sequence carefully:
        C%B K 1 & A W 5 P E 4 Q @ 7 F 6 G © Z J L 2 € D ¥ M #8
        
        How many such symbols are there in the above sequence, each of which is immediately preceded by a consonant and immediately followed by a number?""",
        "options": ["None", "One", "Two", "Four", "None of these"],
        "correct_answer": "Two"
    },
    # ... other questions ...
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

def create_dashboard():
    """Create the main dashboard interface"""
    st.set_page_config(page_title="Adari Institute - ICET Test Series", layout="wide")
    
    # Header with logo and navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image("https://via.placeholder.com/50x50", caption="Adari Institute")
    with col2:
        st.title("ICET Test Series 2024")
    with col3:
        if 'user_name' in st.session_state:
            st.write(f"Welcome, {st.session_state.user_name}")
        
    # Sidebar for navigation
    with st.sidebar:
        st.header("LEARN")
        st.button("📚 Study Material")
        st.button("🎓 Mock Tests")
        st.button("📝 Previous Papers")
        st.button("⚡ Quick Practice")
        
        st.header("TEST SERIES")
        selected_section = st.radio(
            "Select Section",
            ["Quantitative Aptitude", "Verbal Ability", "Logical Reasoning", "Data Analysis"]
        )
        
        st.markdown("## Why Take this Series?")
        st.markdown("""
        - 📈 Comprehensive Coverage
        - 🎯 Topic-wise Practice
        - 📊 Detailed Analytics
        - 🏆 All India Rank
        """)
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["Mock Tests", "Analytics", "Performance"])
    
    with tab1:
        st.header("Success in ICET with 500+ Questions")
        st.write("285 Total Tests | 10 Free Tests")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Select Subject", ["All Subjects", "Quantitative Aptitude", "Verbal Ability", "Logical Reasoning"])
        with col2:
            st.selectbox("Language", ["English", "Telugu"])
            
        # Test Cards
        for i in range(3):
            with st.container():
                st.markdown("---")
                col1, col2 = st.columns([3,1])
                with col1:
                    if i == 0:
                        st.markdown("### 🆓 Introduction to ICET")
                    else:
                        st.markdown(f"### Test {i+1}: Advanced Concepts")
                    st.write(f"👥 {1000 + i*500} Users")
                    st.write(f"⏱️ 30 Questions | 30 Minutes | 30 Marks")
                    st.write("Available in: English, Telugu")
                with col2:
                    if st.button("Start Now", key=f"start_{i}"):
                        st.session_state.selected_test = i
                        st.session_state.test_started = True
                        st.experimental_rerun()

def test_interface():
    """Handle the test taking interface"""
    st.title("Test Interface")
    
    # Update timer
    current_time = time.time()
    if st.session_state.question_start_time:
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
    st.markdown(f"<div class='question-text'>{current_q['question']}</div>", unsafe_allow_html=True)
    
    # Answer options
    answer = st.radio("Select your answer:", current_q["options"], key=f"q_{st.session_state.current_question}")
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Previous"):
            st.session_state.current_question = max(0, st.session_state.current_question - 1)
    with col2:
        if st.button("Mark for Review"):
            pass  # Implement marking logic
    with col3:
        if st.button("Next"):
            if st.session_state.current_question < len(questions) - 1:
                st.session_state.current_question += 1
    
    # Submit test button
    if st.button("Submit Test"):
        st.session_state.test_complete = True
        st.experimental_rerun()

def main():
    # Initialize session state
    initialize_session_state()
    
    # Custom CSS
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
    
    # Main application flow
    if not st.session_state.test_started:
        # Show dashboard
        create_dashboard()
        
        # Get user details if not already present
        with st.sidebar:
            if 'user_name' not in st.session_state:
                st.session_state.user_name = st.text_input("Enter your name")
                st.session_state.user_email = st.text_input("Enter your email")
    
    elif not st.session_state.test_complete:
        # Show test interface
        test_interface()
        
    else:
        # Show results
        st.success("Test Complete! 🎉")
        st.markdown(f"<p class='score-display'>Final Score: {st.session_state.score}/{len(questions)*CORRECT_MARKS}</p>", 
                   unsafe_allow_html=True)
        
        if st.button("Return to Dashboard"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()

if __name__ == "__main__":
    main()