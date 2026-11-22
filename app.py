import streamlit as st

from quiz_core import LETTERS, generate_quiz

st.set_page_config(page_title="AI Quiz Generator", page_icon="📝")
st.title("📝 AI Quiz Generator")
st.write("Type a topic and get a quiz in seconds.")

# ---------- Inputs ----------
topic = st.text_input("Topic (for example: Operating systems)")

col1, col2 = st.columns(2)
count = col1.slider("Number of questions", 1, 10, 5)
difficulty = col2.selectbox("Difficulty", ["easy", "medium", "hard"], index=1)

# ---------- Generate ----------
if st.button("Generate quiz"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Generating your quiz..."):
            try:
                st.session_state.quiz = generate_quiz(topic, count, difficulty)
                st.session_state.quiz_id = st.session_state.get("quiz_id", 0) + 1
            except RuntimeError as error:
                st.error(str(error))

# ---------- Show and mark the quiz ----------
quiz = st.session_state.get("quiz")

if quiz:
    quiz_id = st.session_state.quiz_id
    st.divider()

    with st.form("quiz_form"):
        for i, item in enumerate(quiz):
            st.markdown(f"**Q{i + 1}. {item['question']}**")
            labeled = [f"{l}. {o}" for l, o in zip(LETTERS, item["options"])]
            st.radio(
                "Choose one",
                labeled,
                index=None,
                key=f"q{quiz_id}_{i}",
                label_visibility="collapsed",
            )
        submitted = st.form_submit_button("Submit answers")

    if submitted:
        score = 0
        st.divider()
        for i, item in enumerate(quiz):
            choice = st.session_state.get(f"q{quiz_id}_{i}")
            correct = str(item["answer"]).strip().upper()

            if choice is None:
                st.warning(f"Q{i + 1}: not answered. Correct answer: {correct}. {item['explanation']}")
            elif choice[0] == correct:
                score += 1
                st.success(f"Q{i + 1}: correct! {item['explanation']}")
            else:
                st.error(f"Q{i + 1}: wrong. Correct answer: {correct}. {item['explanation']}")

        st.subheader(f"Score: {score}/{len(quiz)}")