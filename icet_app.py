import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def create_test_app():
    st.set_page_config(page_title="Adari Institute - ICET Test Series", layout="wide")
    
    # Header with logo and navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image("https://via.placeholder.com/50x50", caption="Adari Institute")
    with col2:
        st.title("ICET Test Series 2024")
    with col3:
        st.write("Welcome, Student")
        
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
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["Mock Tests", "Analytics", "Performance"])
    
    with tab1:
        # Test Series Header
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
                    st.button("Start Now", key=f"start_{i}")
                    
        # Why Take This Series section
        st.sidebar.markdown("## Why Take this Series?")
        st.sidebar.markdown("""
        - 📈 Comprehensive Coverage
        - 🎯 Topic-wise Practice
        - 📊 Detailed Analytics
        - 🏆 All India Rank
        """)
        
def initialize_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 1
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'timer' not in st.session_state:
        st.session_state.timer = datetime.now() + timedelta(minutes=30)

def test_interface():
    st.title("Test Interface")
    
    # Timer
    remaining = st.session_state.timer - datetime.now()
    st.write(f"Time Left: {remaining.seconds//60}:{remaining.seconds%60:02d}")
    
    # Question display
    st.subheader(f"Question {st.session_state.current_question}")
    sample_question = "Sample question text here..."
    st.write(sample_question)
    
    # Options
    options = ['Option A', 'Option B', 'Option C', 'Option D']
    selected_option = st.radio("Select your answer:", options, key=f"q_{st.session_state.current_question}")
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Previous"):
            st.session_state.current_question = max(1, st.session_state.current_question - 1)
    with col2:
        if st.button("Mark for Review"):
            st.session_state.answers[st.session_state.current_question] = {'answer': selected_option, 'marked': True}
    with col3:
        if st.button("Next"):
            st.session_state.current_question = min(30, st.session_state.current_question + 1)

def main():
    initialize_session_state()
    if 'test_started' not in st.session_state:
        create_test_app()
        if st.button("Start Test"):
            st.session_state.test_started = True
            st.experimental_rerun()
    else:
        test_interface()

if __name__ == "__main__":
    main()