import ollama
import streamlit as st

st.title("🏥 Hospital Course Summariser ")

hospital_course = st.text_area("Hospital Course", height=300)

if st.button("Summarise"):
    if hospital_course.strip():
        prompt = f"""
Paraphrase and comprehensively summarise the following hospital course in 4–6 lines. 
Do not omit any clinical information. Use passive voice, third person, and past tense. 
Write in a single paragraph (no bullet points). 
Ensure the summary ends with a complete, structured sentence that includes 'managed' and 'transferred to SNF'. 

Hospital course:
{hospital_course}
"""
        with st.spinner("Generating summary..."):
            response = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )
            summary = response["message"]["content"]
            st.subheader("📝 Summary")
            st.write(summary)
    else:
        st.warning("⚠️ Please paste the hospital course first.")
