import os
import streamlit as st
from openai import OpenAI

# Get API key from environment
api_key = os.environ.get("OPENAI_API_KEY")

st.title("🏥 Hospital Course Summariser")
st.write("Paste the full hospital course below, and get a concise, structured summary.")

# If no API key, warn the user and stop execution
if not api_key:
    st.error("⚠️ OPENAI_API_KEY is not set. Please add it to your environment before using this app.")
    st.stop()

# Initialise OpenAI client
client = OpenAI(api_key=api_key)

# Text input
hospital_course = st.text_area("Hospital Course", height=300)

if st.button("Summarise"):
    if not hospital_course.strip():
        st.warning("⚠️ Please paste the hospital course text first.")
    else:
        # Prompt with your rules
        prompt = f"""
Paraphrase and comprehensively summarise the following hospital course in 4–6 lines. 
Do not omit any clinical information. Use passive voice, third person, and past tense. 
Write in a single paragraph (no bullet points). 
Ensure the summary ends with a complete, structured sentence that includes 'managed' and 'transferred to SNF'. 

Hospital course:
{hospital_course}
"""

        with st.spinner("Generating summary..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a medical summarisation assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                summary = response.choices[0].message.content
                st.subheader("📝 Summary")
                st.write(summary)

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")



'''import streamlit as st
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
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                )
                summary = response.choices[0].message.content.strip()
                st.session_state.last_summary = summary
                st.success("✅ Summary generated:")
                st.write(summary)
        else:
            st.warning("⚠️ Please paste a hospital course first.")

# --- CHAT MODE ---
elif mode == "Chat":
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.experimental_rerun()

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

    # Chat input box
    user_input = st.text_input("💬 Ask a question or refine the summary:", key="chat_input")
    if st.button("Send"):
        if user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.chat_history
                )
                reply = response.choices[0].message.content.strip()
                st.session_state.chat_history.append({"role": "assistant", "content": reply})

            st.experimental_rerun()  # Refresh to show new bubbles
'''