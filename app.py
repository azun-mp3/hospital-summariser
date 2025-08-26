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
                    model="gpt-3.5-turbo",
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

