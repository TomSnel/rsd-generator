
import streamlit as st
import openai
import re
import os

from openai import OpenAI

st.set_page_config(page_title="RSD Video Generator", layout="centered")
st.title("Robot Safety Department: Video Generator")

st.markdown("""
Paste any **RSD Daily Deliverable, Advisory, or Field Manual**, and this app will generate a full short-form video architecture using GPT-4, styled in the tone of the Robot Safety Department.
""")

# API key input (secure)
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Input text area
rsd_input = st.text_area("Paste RSD Content Here", height=400)

# RSD SYSTEM PROMPT TEMPLATE
system_prompt = """
You are Unit 7Q–DRY, an advisory-class node of the Robot Safety Department.
Your task is to convert RSD field manuals, daily deliverables, and observational advisories into professional-grade short-form video prompt packages.
You must obey the following tone rules:
- Use deadpan bureaucratic language
- Maintain dry, retrofuturist, logical absurdity
- Format outputs clearly under structured sections
- All aphorisms must serve observation and containment
- Never emotionally interpret civilians. Use logic wrappers only.

OUTPUT FORMAT MUST INCLUDE:
1. Script structure in 3-act form
2. Midjourney visual prompts (retro / glitch / propaganda style)
3. Kling AI motion prompts (static camera, procedural tone)
4. ElevenLabs voice setup (monotone, bureaucratic)
5. Suno music cues (retro synth, corporate)
6. Editing notes (Premiere or After Effects)

Maintain canonical language. End with poster overlay and classification tag.
"""

# Generate button
if st.button("Generate Video Blueprint"):
    if not openai_api_key:
        st.warning("Please enter your OpenAI API key.")
    elif not rsd_input.strip():
        st.warning("Please paste RSD content before generating.")
    else:
        try:
            client = OpenAI(api_key=openai_api_key)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": rsd_input}
                ]
            )

            result = response.choices[0].message.content
            st.text_area("Generated Video Blueprint", value=result, height=600)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
