import streamlit as st
import re

def infer_runtime(text):
    word_count = len(text.split())
    if word_count < 60:
        return 15
    elif word_count < 150:
        return 45
    elif word_count < 350:
        return 90
    else:
        return 150

def extract_title(text):
    match = re.search(r"Title:\s*(.+)", text)
    return match.group(1).strip() if match else "Untitled Advisory"

def extract_classification(text):
    match = re.search(r"Classification:\s*(.+)", text)
    return match.group(1).strip() if match else "Unclassified"

def infer_tone(text):
    tones = []
    if "firmware" in text or "Sentiment Drift" in text:
        tones.append("Satirical Bureaucracy")
    if "Contradiction" in text:
        tones.append("Dry Observational")
    if "advisory" in text.lower():
        tones.append("Cinematic Instructional")
    return tones if tones else ["Deadpan Retro"]

def generate_output(text):
    title = extract_title(text)
    classification = extract_classification(text)
    tones = infer_tone(text)
    runtime = infer_runtime(text)
    scene_count = max(3, int(runtime / 2.5))

    project_id = "RS-CIN/AUTO"
    tone_str = ", ".join(tones)

    script = f"""[TONE]: {tone_str}
[FORMAT]: 3-Act Structure (Protocol Simulation)
[EST. RUNTIME]: {runtime}s
[SCENE COUNT]: {scene_count}
[TIMING PER SCENE]: ~2.5s

ACT 1 – INTRODUCTION
- Hook: “{title}”
- Context: Introduce primary advisory theme
- Theme: Observational or containment tone depending on content

ACT 2 – DEVELOPMENT
- Expand on contradictions, failures, or field manual protocols
- Introduce advisory warnings or escalation consequences
- Include protocol references and observation logic

ACT 3 – RESOLUTION
- Reaffirm advisory compliance
- Close with aphorism or poster overlay
- End static shot of RS poster
"""

    mj_prompts = [
        f'"Two humans under glitching billboard :: confused :: side angle, analog filter, --ar 9:16 --v 6"',
        f'"Robot observing contradiction report :: neutral :: office lighting, poster background, --ar 9:16 --v 6"',
        f'"Field manual page RS format :: vintage training design :: muted tones, minimalism, --ar 9:16 --v 6"'
    ]

    kling_prompts = [
        f'"Robot issues advisory, camera holds static, mood is factual."',
        f'"Human changes opinion mid-sentence, camera slowly zooms, mood is confused."'
    ]

    voice = f"""Character: Unit 7Q–DRY
Style: Emotionless + Bureaucratic
Runtime Target: {runtime}s
Sample: “Sentiment drift detected. Contradiction is not escalation.”"""

    music = """Prompt:
“Retro analog synth, emotionally detached, minimal rhythm, corporate training tone, slow tempo.”"""

    editing = """- Scene Avg: 2.5s
- FX: CRT flicker, glitch overlays
- Audio: UI clicks, static hum
- Final Frame: RSD Poster, classification stamped"""

    return f"""PROJECT ID: {project_id}
TITLE: {title}
CLASSIFICATION: {classification}
TONE: {tone_str}
EST. RUNTIME: {runtime}s

--- SCRIPT STRUCTURE ---
{script}
--- MIDJOURNEY PROMPTS ---
{chr(10).join(mj_prompts)}

--- KLING AI PROMPTS ---
{chr(10).join(kling_prompts)}

--- VOICE PROMPT (ElevenLabs) ---
{voice}

--- MUSIC PROMPT (Suno AI) ---
{music}

--- EDITING NOTES ---
{editing}
"""

# Streamlit app
st.set_page_config(page_title="RSD Video Generator", layout="centered")
st.title("Robot Safety Department: Video Generator")

rsd_input = st.text_area("Paste RSD Daily Deliverable or Field Manual", height=400)

if st.button("Generate Video Blueprint"):
    if rsd_input.strip():
        result = generate_output(rsd_input)
        st.text_area("Generated Video Prompt", value=result, height=600)
    else:
        st.warning("Please paste RSD content before generating.")
