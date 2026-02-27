import streamlit as st
import requests
import uuid
import speech_recognition as sr

API_URL = "http://localhost:8000/voice/turn"

st.set_page_config(page_title="Voice Support Demo", layout="centered")
st.title("🎙 Voice Support Engine Demo")

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------- Display Chat --------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            st.caption(
                f"Intent: {msg['intent']} | "
                f"Confidence: {msg['confidence']} | "
                f"Escalate: {msg['escalate']}"
            )

st.markdown("### 🎤 Voice Input")

audio_text = None

if st.button("Start Speaking"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)

        try:
            audio_text = recognizer.recognize_google(audio)
            st.success(f"You said: {audio_text}")
        except Exception:
            st.error("Could not recognize speech.")

# -------- Manual fallback input --------
manual_input = st.chat_input("Or type your question...")

if manual_input:
    audio_text = manual_input

if audio_text:

    st.session_state.messages.append(
        {"role": "user", "content": audio_text}
    )

    with st.chat_message("user"):
        st.markdown(audio_text)

    payload = {
        "transcript": audio_text,
        "user_id": 1,
        "project_id": 0,
        "conversation_id": str(uuid.uuid4()),
        "context_summary": {}
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=15)
        data = response.json()

        reply_text = data.get("reply_text")
        intent = data.get("intent")
        confidence = data.get("confidence")
        escalate = data.get("escalate")

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply_text,
            "intent": intent,
            "confidence": confidence,
            "escalate": escalate
        })

        with st.chat_message("assistant"):
            st.markdown(reply_text)
            st.caption(
            f"Intent: {intent} | "
            f"Confidence: {confidence} | "
            f"Escalate: {escalate}"
    )

    # -------- Browser TTS --------
            safe_reply = reply_text.replace('"', '\\"')

            st.components.v1.html(f"""
              <script>
              const synth = window.speechSynthesis;
             const utterance = new SpeechSynthesisUtterance("{safe_reply}");
             utterance.lang = "en-US";
             synth.cancel();  // stop previous speech
             synth.speak(utterance);
             </script>
             """, height=0)

    except Exception as e:
        st.error(f"Error: {str(e)}")