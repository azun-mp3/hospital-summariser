import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.set_page_config(page_title="Hospital Course Summariser + Chat", layout="centered")
st.title("🏥 Hospital Course Summariser + Chat Assistant")

# Mode selector
mode = st.radio("Choose mode:", ["Summarise", "Chat"])

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_summary" not in st.session_state:
    st.session_state.last_summary = ""

# --- SUMMARISE MODE ---
if mode == "Summarise":
    hospital_course = st.text_area("Paste the hospital course here:", height=200)

    if st.button("Summarise"):
        if hospital_course.strip():
            prompt = (
                "Paraphrase and comprehensively summarise the following hospital course "
                "in 4-6 lines. Do not miss any information. Write in passive voice, "
                "3rd person, past tense. Remove bullet points and keep everything in a paragraph. "
                "End with 'managed' and 'transferred to SNF' in a complete structured sentence.\n\n"
                f"{hospital_course}"
            )

            with st.spinner("Summarising..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",  # use free API model
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3
                    )
                    summary = response.choices[0].message.content.strip()
                    st.session_state.last_summary = summary
                    st.success("✅ Summary generated:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")
        else:
            st.warning("⚠️ Please paste a hospital course first.")

# --- CHAT MODE ---
elif mode == "Chat":
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []

    # Auto-insert last summary if chat is empty
    if st.session_state.last_summary and not st.session_state.chat_history:
        st.session_state.chat_history.append(
            {"role": "assistant", "content": f"Here’s the last summary:\n\n{st.session_state.last_summary}"}
        )

    # Display chat in bubbles
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f"<div style='text-align: right; color: white; background-color: #1E90FF; padding: 8px; border-radius: 12px; margin: 5px 0; display: inline-block;'>{msg['content']}</div>",
                unsafe_allow_html=True,
            )
        else:  # assistant
            st.markdown(
                f"<div style='text-align: left; color: black; background-color: #F0F0F0; padding: 8px; border-radius: 12px; margin: 5px 0; display: inline-block;'>{msg['content']}</div>",
                unsafe_allow_html=True,
            )

    # Chat input box using a form
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 Ask a question or refine the summary:", key="chat_input")
        submit_button = st.form_submit_button("Send")

    if submit_button and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # free API model
                    messages=[{"role": "system", "content": "You are a helpful medical assistant."}] + st.session_state.chat_history,
                    temperature=0.3
                )
                reply = response.choices[0].message.content.strip()
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
