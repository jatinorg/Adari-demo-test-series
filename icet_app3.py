import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

# Sample questions data
SAMPLE_QUESTIONS = {
    1: {
        "question": "If A can do a work in 15 days and B in 20 days, in how many days can they do it together?",
        "options": ["8.57 days", "9.57 days", "10.57 days", "11.57 days"],
        "correct_answer": 0,
        "explanation": "Using the formula: (a×b)/(a+b) = (15×20)/(15+20) = 300/35 = 8.57 days"
    },
    2: {
        "question": "The average of first 50 natural numbers is:",
        "options": ["25.30", "25.40", "25.50", "25.60"],
        "correct_answer": 2,
        "explanation": "Sum of first n natural numbers = n(n+1)/2. Here n=50, so average = 50×51/(2×50) = 25.50"
    },
    3: {
        "question": "A train running at the speed of 60 km/hr crosses a pole in 9 seconds. What is the length of the train?",
        "options": ["120 meters", "140 meters", "150 meters", "160 meters"],
        "correct_answer": 2,
        "explanation": "Speed = 60 km/hr = 16.67 m/s. Length = Speed × Time = 16.67 × 9 = 150 meters"
    },
    # Add more sample questions as needed
}

def create_test_app():
    st.set_page_config(page_title="Adari Institute - ICET Test Series", layout="wide", initial_sidebar_state="expanded")
    
    # Custom CSS for dark theme and styling
    st.markdown("""
        <style>
        .stApp {
            background-color: #1a1a1a;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #2d2d2d;
        }
        .study-material-link {
            background-color: transparent;
            color: #ff4b4b;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 4px;
            border: 1px solid #ff4b4b;
            cursor: pointer;
            display: inline-block;
            margin: 4px 0;
            width: 100%;
            text-align: left;
        }
        .study-material-link:hover {
            background-color: rgba(255, 75, 75, 0.1);
        }
        .question-card {
            background-color: #2d2d2d;
            padding: 20px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .result-card {
            background-color: #2d2d2d;
            padding: 20px;
            border-radius: 8px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    
    
    # Rest of the create_test_app function remains the same as before
    # ... (previous code) ...

def test_interface():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 1
        st.session_state.answers = {}
        st.session_state.start_time = datetime.now()
        st.session_state.end_time = st.session_state.start_time + timedelta(minutes=30)

    # Display timer
    remaining = st.session_state.end_time - datetime.now()
    if remaining.total_seconds() <= 0:
        show_results()
        return

    st.markdown(f"### Time Left: {remaining.seconds//60}:{remaining.seconds%60:02d}")

    # Display current question
    question_data = SAMPLE_QUESTIONS[st.session_state.current_question]
    
    with st.container():
        st.markdown(f"### Question {st.session_state.current_question}")
        st.write(question_data["question"])
        
        # Radio buttons for options
        selected_option = st.radio(
            "Select your answer:",
            question_data["options"],
            key=f"q_{st.session_state.current_question}"
        )
        
        # Store answer when selected
        if selected_option:
            st.session_state.answers[st.session_state.current_question] = {
                'selected_option': question_data["options"].index(selected_option),
                'correct_answer': question_data["correct_answer"]
            }

    # Navigation buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("Previous") and st.session_state.current_question > 1:
            st.session_state.current_question -= 1
            st.experimental_rerun()
            
    with col2:
        if st.button("Mark for Review"):
            if st.session_state.current_question not in st.session_state.answers:
                st.session_state.answers[st.session_state.current_question] = {
                    'marked_for_review': True
                }
            
    with col3:
        if st.button("Next") and st.session_state.current_question < len(SAMPLE_QUESTIONS):
            st.session_state.current_question += 1
            st.experimental_rerun()
            
    with col4:
        if st.button("Submit Test"):
            show_results()

def calculate_results():
    correct = 0
    incorrect = 0
    unattempted = 0
    
    for q_num in range(1, len(SAMPLE_QUESTIONS) + 1):
        if q_num in st.session_state.answers:
            if 'selected_option' in st.session_state.answers[q_num]:
                if st.session_state.answers[q_num]['selected_option'] == SAMPLE_QUESTIONS[q_num]['correct_answer']:
                    correct += 1
                else:
                    incorrect += 1
        else:
            unattempted += 1
            
    return {
        'correct': correct,
        'incorrect': incorrect,
        'unattempted': unattempted,
        'score': correct * 4 - incorrect,  # 4 marks for correct, -1 for incorrect
        'accuracy': (correct / (correct + incorrect)) * 100 if (correct + incorrect) > 0 else 0
    }

def show_results():
    st.session_state.test_completed = True
    results = calculate_results()
    
    st.title("Test Results")
    
    # Summary Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Score", f"{results['score']}/{len(SAMPLE_QUESTIONS)*4}")
    with col2:
        st.metric("Accuracy", f"{results['accuracy']:.1f}%")
    with col3:
        st.metric("Time Taken", f"{(datetime.now() - st.session_state.start_time).seconds//60} minutes")

    # Detailed Analysis
    st.markdown("### Question-wise Analysis")
    
    for q_num, q_data in SAMPLE_QUESTIONS.items():
        with st.expander(f"Question {q_num}"):
            st.write(q_data["question"])
            st.write("Correct Answer:", q_data["options"][q_data["correct_answer"]])
            if q_num in st.session_state.answers and 'selected_option' in st.session_state.answers[q_num]:
                selected = st.session_state.answers[q_num]['selected_option']
                st.write("Your Answer:", q_data["options"][selected])
                if selected == q_data["correct_answer"]:
                    st.success("Correct! +4 marks")
                else:
                    st.error("Incorrect! -1 mark")
            else:
                st.warning("Not attempted")
            st.write("Explanation:", q_data["explanation"])

    # Performance Chart
    chart_data = pd.DataFrame({
        'Category': ['Correct', 'Incorrect', 'Unattempted'],
        'Count': [results['correct'], results['incorrect'], results['unattempted']]
    })
    
    fig = px.pie(chart_data, values='Count', names='Category', 
                 title='Performance Analysis',
                 color_discrete_sequence=['#00ff00', '#ff0000', '#808080'])
    st.plotly_chart(fig)

def main():
    if 'test_completed' not in st.session_state:
        st.session_state.test_completed = False

    if not st.session_state.test_completed:
        test_interface()
    else:
        show_results()
        if st.button("Start New Test"):
            for key in ['current_question', 'answers', 'start_time', 'end_time', 'test_completed']:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()

if __name__ == "__main__":
    main()