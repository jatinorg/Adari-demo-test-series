import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Set page config
st.set_page_config(
    page_title="Adari Institute - ICET Test Series",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
    }
    .test-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin: 10px 0;
        border: 1px solid #dee2e6;
    }
    .score-display {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .dataframe {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
def sidebar():
    with st.sidebar:
        st.title("ICET Test Series")
        
        # Navigation menu
        selected = st.radio(
            "Navigation",
            ["Home", "Test Series", "Live Tests", "Practice", "Performance Analytics"]
        )
        
        # User profile section
        st.sidebar.markdown("---")
        st.sidebar.markdown("### User Profile")
        st.sidebar.text("Student Name: John Doe")
        st.sidebar.text("ID: ADA2024001")
        
        return selected

# Home page
def home():
    st.title("Welcome to Adari Institute ICET Test Series")
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Tests Attempted", value="15")
    with col2:
        st.metric(label="Average Score", value="75%")
    with col3:
        st.metric(label="Tests Available", value="30")
    
    # Recent activity
    st.subheader("Recent Activity")
    recent_tests = pd.DataFrame({
        'Test Name': ['Full Mock Test 1', 'Sectional Test - Quant', 'Topic Test - DI'],
        'Date': ['2024-12-14', '2024-12-13', '2024-12-12'],
        'Score': ['82/100', '45/50', '28/30']
    })
    # Set the index to None to hide it
    recent_tests.index = ['' for _ in range(len(recent_tests))]
    st.dataframe(recent_tests)

# Test series page
def test_series():
    st.title("Available Test Series")
    
    # Filter section
    col1, col2 = st.columns([3, 1])
    with col2:
        test_type = st.selectbox("Filter by:", 
            ["All Tests", "Full Length", "Sectional", "Topic Wise"])
    
    # Display tests
    for i in range(3):
        with st.container():
            st.markdown(f"""
            <div class="test-card">
                <h3>ICET Full Mock Test {i+1}</h3>
                <p>Duration: 2 hours | Questions: 100 | Max Marks: 100</p>
                <p>Last Attempted: {datetime.now().strftime('%b %d, %Y')}</p>
            </div>
            """, unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,1,2])
            with col1:
                st.button(f"Start Test {i+1}", key=f"start_{i}")
            with col2:
                st.button(f"View Syllabus {i+1}", key=f"syllabus_{i}")
            with col3:
                st.progress(0.8, text="80% Success Rate")

# Test interface
def test_interface():
    st.title("Test in Progress")
    
    # Timer and progress
    col1, col2 = st.columns([3,1])
    with col1:
        st.progress(0.6, text="60/100 Questions")
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 5px;'>
            Time Remaining: 01:30:00
        </div>
        """, unsafe_allow_html=True)
    
    # Question display
    st.markdown("### Question 1")
    st.write("Sample question text goes here...")
    
    # Options
    options = ['Option A', 'Option B', 'Option C', 'Option D']
    selected_option = st.radio("Select your answer:", options)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.button("Previous")
    with col2:
        st.button("Mark for Review")
    with col3:
        st.button("Next")

# Main app logic
def main():
    selected = sidebar()
    
    if selected == "Home":
        home()
    elif selected == "Test Series":
        test_series()
    elif selected == "Live Tests":
        st.title("Live Tests")
        st.write("No live tests currently scheduled.")
    elif selected == "Practice":
        st.title("Practice Section")
        st.write("Choose topics to practice...")
    elif selected == "Performance Analytics":
        st.title("Your Performance Analytics")
        # Sample performance data
        performance_data = pd.DataFrame({
            'Test Score': [75, 82, 78, 85, 90]
        }, index=['Test 1', 'Test 2', 'Test 3', 'Test 4', 'Test 5'])
        st.line_chart(performance_data)

if __name__ == "__main__":
    main()