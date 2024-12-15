import streamlit as st
import pandas as pd
import random

class AdariInstituteApp:
    def _init_(self):
        # Configure page
        st.set_page_config(page_title="Adari Institute", page_icon=":book:", layout="wide")
        
        # Initialize session state for tracking
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'current_exam' not in st.session_state:
            st.session_state.current_exam = None
        if 'current_test' not in st.session_state:
            st.session_state.current_test = None
        
        # Sample exam data (would typically come from a database)
        self.exams = {
            "ICET": {
                "full_name": "Integrated ICET Exam",
                "subjects": ["Logical Reasoning", "Quantitative Aptitude", "English"]
            },
            "TSPSC": {
                "full_name": "Telangana State Public Service Commission",
                "subjects": ["General Knowledge", "Arithmetic", "Reasoning"]
            },
            "GATE": {
                "full_name": "Graduate Aptitude Test in Engineering",
                "subjects": ["Engineering Mathematics", "Technical Subjects", "Aptitude"]
            }
        }
        
        # Sample questions (would typically be from a database)
        self.questions = {
            "Logical Reasoning": [
                {
                    "question": "If A > B and B > C, then A is definitely greater than C",
                    "options": ["True", "False", "Depends on the context", "Cannot be determined"],
                    "correct_answer": "True"
                },
                {
                    "question": "What comes next in the sequence: 2, 6, 12, 20, ?",
                    "options": ["30", "28", "26", "24"],
                    "correct_answer": "30"
                }
            ],
            "Quantitative Aptitude": [
                {
                    "question": "If 2x + 3 = 15, what is the value of x?",
                    "options": ["4", "5", "6", "7"],
                    "correct_answer": "6"
                }
            ]
        }
    
    def login_page(self):
        """Login page for the application"""
        st.title("Adari Institute - Login")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.image("https://via.placeholder.com/300x200?text=Adari+Institute+Logo")
        
        with col2:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                # Simple login validation (replace with proper authentication)
                if username == "student" and password == "adari2024":
                    st.session_state.logged_in = True
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
    
    def dashboard(self):
        """Main dashboard for logged-in users"""
        st.title("Welcome to Adari Institute")
        
        # Exam Selection
        st.subheader("Choose Your Exam")
        selected_exam = st.selectbox("Select Exam", list(self.exams.keys()))
        
        # Exam Details
        exam_details = self.exams[selected_exam]
        st.write(f"*Exam:* {exam_details['full_name']}")
        st.write("*Subjects Covered:*")
        for subject in exam_details['subjects']:
            st.write(f"- {subject}")
        
        # Start Test Button
        if st.button("Start Test Series"):
            st.session_state.current_exam = selected_exam
            st.experimental_rerun()
    
    def test_series_page(self):
        """Page for conducting test series"""
        st.title(f"{self.exams[st.session_state.current_exam]['full_name']} - Test Series")
        
        # Select a random subject for demonstration
        subject = random.choice(self.exams[st.session_state.current_exam]['subjects'])
        st.subheader(f"Subject: {subject}")
        
        # Prepare questions
        questions = self.questions.get(subject, [])
        
        # Display questions
        user_answers = {}
        for i, q in enumerate(questions, 1):
            st.write(f"*Question {i}:* {q['question']}")
            user_answers[i] = st.radio(
                f"Select your answer for Question {i}", 
                q['options'], 
                key=f"q{i}"
            )
        
        # Submit Test Button
        if st.button("Submit Test"):
            self.evaluate_test(questions, user_answers)
    
    def evaluate_test(self, questions, user_answers):
        """Evaluate the test and show results"""
        total_questions = len(questions)
        correct_answers = sum(
            1 for i, q in enumerate(questions, 1) 
            if user_answers[i] == q['correct_answer']
        )
        
        percentage = (correct_answers / total_questions) * 100
        
        st.subheader("Test Results")
        st.write(f"Total Questions: {total_questions}")
        st.write(f"Correct Answers: {correct_answers}")
        st.write(f"Percentage: {percentage:.2f}%")
        
        # Performance evaluation
        if percentage >= 90:
            st.success("Excellent Performance! 🌟")
        elif percentage >= 75:
            st.info("Great Job! Keep Practicing! 👍")
        else:
            st.warning("You can improve. Review your answers carefully. 📚")
    
    def main(self):
        """Main application flow"""
        if not st.session_state.logged_in:
            self.login_page()
        elif st.session_state.current_exam is None:
            self.dashboard()
        else:
            self.test_series_page()

# Run the application
if __name__ == "_main_":
    app = AdariInstituteApp()
    app.main()