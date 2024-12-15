import streamlit as st
import time

def main():
    st.sidebar.image("logo.png", width=100)
    st.sidebar.title("Adari Institute")
    st.title("Online Test Series")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
    else:
        display_test_series()

def login():
    st.subheader("Login")
    name = st.text_input("Enter your name")
    if st.button("Login") and name:
        st.session_state.logged_in = True
        st.session_state.name = name
        st.success(f"Welcome {name}!")

def display_test_series():
    st.sidebar.header("Available Test Series")
    test_series = ["Test Series 1", "Test Series 2", "Test Series 3"]
    selected_series = st.sidebar.selectbox("Select a Test Series", test_series)
    if selected_series:
        start_test(selected_series)

def start_test(test_name):
    questions = {
        "Test Series 1": [
            {"question": "What is 2 + 2?", "answer": 4},
            {"question": "What is 3 + 5?", "answer": 8}
        ],
        "Test Series 2": [
            {"question": "What is 10 - 4?", "answer": 6},
            {"question": "What is 7 + 2?", "answer": 9}
        ],
        "Test Series 3": [
            {"question": "What is 5 * 3?", "answer": 15},
            {"question": "What is 6 / 2?", "answer": 3}
        ]
    }
    
    total_time = 30 * 60  # 30 minutes in seconds
    if f'{test_name}_start_time' not in st.session_state:
        st.session_state[f'{test_name}_start_time'] = time.time()

    time_left = total_time - (time.time() - st.session_state[f'{test_name}_start_time'])

    if time_left <= 0:
        st.warning("Time's up! Submitting the test...")
        calculate_score(test_name, questions[test_name])
        return

    st.subheader(f"{test_name}")
    mins, secs = divmod(int(time_left), 60)
    st.info(f"Time Left: {mins}m {secs}s")

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.answers = {}

    current_q = questions[test_name][st.session_state.current_question]

    st.write(current_q['question'])
    user_answer = st.number_input("Your answer", step=1, format="%d")

    if st.button("Previous") and st.session_state.current_question > 0:
        st.session_state.current_question -= 1

    if st.button("Next") and st.session_state.current_question < len(questions[test_name]) - 1:
        st.session_state.answers[st.session_state.current_question] = user_answer
        st.session_state.current_question += 1

    if st.button("Submit Test"):
        st.session_state.answers[st.session_state.current_question] = user_answer
        calculate_score(test_name, questions[test_name])

def calculate_score(test_name, questions):
    score = 0
    correct = 0
    incorrect = 0
    solutions = []

    for idx, q in enumerate(questions):
        correct_answer = q['answer']
        user_answer = st.session_state.answers.get(idx, None)
        solutions.append((q['question'], correct_answer, user_answer))
        if user_answer == correct_answer:
            score += 1
            correct += 1
        else:
            incorrect += 1

    st.success(f"Test Completed: {test_name}")
    st.info(f"Your Score: {score}/{len(questions)}")
    st.write(f"Correct Answers: {correct}")
    st.write(f"Incorrect Answers: {incorrect}")
    st.subheader("Solutions")
    for q, correct_ans, user_ans in solutions:
        st.write(f"Q: {q}")
        st.write(f"Correct Answer: {correct_ans}")
        st.write(f"Your Answer: {user_ans if user_ans is not None else 'Not Answered'}")

if __name__ == '__main__':
    main()
