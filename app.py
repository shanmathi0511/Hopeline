import streamlit as st
import speech_recognition as sr
import tempfile
import os
import fitz  # PyMuPDF
import requests
import base64
import docx
import folium
from streamlit_folium import st_folium

# 🧠 Custom Modules
from chatbot import generate_response
from legal_fetcher import get_legal_references
from emotion_detector import detect_emotion
from legal_summarizer import summarize_text
from text_translator import translate_text
from pdf_generator import generate_pdf
from location_fetcher import get_coordinates_from_city
from intent_detector import detect_intent  # <-- For AI Insights

# -------------------------------
# 🌟 PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="HopeLine", page_icon="🧠", layout="wide")

# 🎨 CUSTOM BACKGROUND CSS

def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 12px;
        }}
        section[data-testid="stSidebar"] > div:first-child {{
            background-color: rgba(255, 255, 255, 0.75);
            border-radius: 10px;
            padding: 1rem;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("wallpaper.jpeg")

# -------------------------------
# 💬 SIDEBAR CHATBOT
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.title("💬 HopeLine Chatbot")
    user_input = st.text_input("Type your message here:", key="sidebar_input")

    if st.button("Send", key="send_btn") and user_input:
        st.session_state.chat_history.append(("You", user_input))
        with st.spinner("HopeLine is thinking..."):
            try:
                bot_reply = generate_response(user_input)
                summarized_reply = summarize_text(bot_reply)
                st.session_state.chat_history.append(("HopeLine", summarized_reply))
            except Exception as e:
                st.session_state.chat_history.append(("HopeLine", f"⚠️ Error: {e}"))

    for sender, message in st.session_state.chat_history[::-1]:
        if sender == "You":
            st.markdown(f"🧍 **{sender}:** {message}")
        else:
            st.markdown(f"🤖 **{sender}:** {message}")

# ================= Sidebar Enhancements ====================
with st.sidebar:
    st.markdown("## 🧭 Quick Access")

    # Quick Legal Help Topics
    st.markdown("**🧾 Quick Legal Help Topics**")
    quick_topics = {
        "Rights in Police Custody": "What are my rights in police custody?",
        "Domestic Violence": "What legal actions can I take in a domestic violence situation?",
        "Child Custody Rights": "What are the child custody laws in India?",
        "Filing an FIR": "How do I file an FIR with the police?",
    }

    for label, query in quick_topics.items():
        if st.button(label):
            st.session_state.user_input = query

    st.divider()

    # Emergency Button
    st.markdown("## 🚨 Emergency Help")
    if st.button("🚨 I'm in immediate danger"):
        st.warning("📞 **Emergency Hotlines:**\n\n"
                   "- 112: National Emergency\n"
                   "- 1091: Women Helpline\n"
                   "- 1098: Child Helpline\n"
                   "- 100: Police\n\n"
                   "📍 _Map to nearest police station coming soon!_")

    st.divider()

    # Recent Topics
    st.markdown("## 🔁 Recent Topics")
    if "recent_queries" not in st.session_state:
        st.session_state.recent_queries = []

    for recent in st.session_state.recent_queries[-5:][::-1]:
        if st.button(f"🔁 {recent[:40]}..."):
            st.session_state.user_input = recent

    st.divider()

    # Chat Mode Toggle
    st.markdown("## 🎛️ Chat Mode")
    chat_mode = st.radio(
        "Choose a mode:",
        options=["🗣️ Emotional Support", "⚖️ Legal Assistance", "🧠 General Help"],
        index=1,
        key="chat_mode"
    )

# -------------------------------
# 🧠 MAIN CONTENT
# -------------------------------
st.title("🧠 HopeLine – Legal Support Assistant")
st.markdown("Welcome to **HopeLine**, your AI-powered assistant for emotional support and legal awareness.")

# -------------------------------
# 🎤 VOICE OR TEXT INPUT
# -------------------------------
query = ""
with st.expander("🎤 Use Voice Input"):
    audio_file = st.file_uploader("Upload your voice query (WAV format):", type=["wav"])
    if audio_file:
        r = sr.Recognizer()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        try:
            with sr.AudioFile(tmp_path) as source:
                audio_data = r.record(source)
                query = r.recognize_google(audio_data)
                st.success(f"Transcribed Text: {query}")
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError:
            st.error("Speech recognition service is unavailable.")
        finally:
            os.remove(tmp_path)

# 👉 Load query from sidebar
if not query:
    if "user_input" in st.session_state and st.session_state.user_input:
        query = st.session_state.user_input
        st.session_state.recent_queries.append(query)
        st.session_state.user_input = ""
    else:
        query = st.text_input("Or type your message here:")

# -------------------------------
# 🤖 PROCESS QUERY
# -------------------------------
if query:
    with st.spinner("HopeLine is processing your query..."):
        try:
            emotion = detect_emotion(query)
            if emotion:
                st.info(f"🧠 Detected emotion: *{emotion}*")

            raw_response = generate_response(query)
            summarized_response = summarize_text(raw_response)

            legal_results = get_legal_references(query)

            lang = st.selectbox("🌍 Translate response to:", ["None", "English", "Hindi", "Tamil", "Telugu"])
            translated_response = (
                translate_text(summarized_response, target_lang=lang)
                if lang != "None" else summarized_response
            )

            st.subheader("📬 HopeLine Response:")
            st.markdown(f"**You said —** {query}")
            st.success(translated_response)

            if legal_results:
                st.markdown("### 📚 Related Legal References:")
                st.markdown(legal_results, unsafe_allow_html=True)
            else:
                st.info("⚖️ No specific legal reference found. Please consult a legal advisor for further help.")

            if st.button("📘️ Download Response as PDF"):
                pdf_path = generate_pdf(query, translated_response, legal_results)
                with open(pdf_path, "rb") as f:
                    st.download_button("📄 Download PDF", f, file_name="Hopeline_Response.pdf")

        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")

# -------------------------------
# 📄 DOCUMENT SUMMARIZATION
# -------------------------------
st.markdown("---")
st.subheader("📄 Upload Legal Document for Summarization")

doc_file = st.file_uploader("Upload a legal document (PDF or DOCX):", type=["pdf", "docx"])

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

if doc_file:
    with st.spinner("Extracting and summarizing document..."):
        try:
            extracted_text = ""
            if doc_file.name.endswith(".pdf"):
                extracted_text = extract_text_from_pdf(doc_file)
            elif doc_file.name.endswith(".docx"):
                extracted_text = extract_text_from_docx(doc_file)

            if extracted_text.strip():
                summary = summarize_text(extracted_text)
                st.success("📝 Summary:")
                st.markdown(summary)
            else:
                st.warning("No readable text found in the uploaded document.")
        except Exception as e:
            st.error(f"❌ Failed to summarize: {e}")

# -------------------------------
# 📍 LEGAL AID LOCATOR
# -------------------------------
st.markdown("---")
st.subheader("📍 Find Legal Aid Near You")

city = st.text_input("Enter your city name:")

def get_nearby_legal_aid(lat, lon, radius=5000):
    query = f"""
    [out:json];
    (
      node["amenity"="police"](around:{radius},{lat},{lon});
      node["office"="lawyer"](around:{radius},{lat},{lon});
      node["amenity"="courthouse"](around:{radius},{lat},{lon});
    );
    out center;
    """
    try:
        response = requests.get("http://overpass-api.de/api/interpreter", params={'data': query})
        return response.json().get("elements", [])
    except Exception as e:
        st.error(f"Error fetching legal aid locations: {e}")
        return []

def show_osm_map(city_name):
    lat, lon = get_coordinates_from_city(city_name)
    if not lat or not lon:
        st.warning("⚠️ Location not found. Please enter a valid city name.")
        return

    m = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], popup=f"📍 {city_name}", icon=folium.Icon(color="red")).add_to(m)

    places = get_nearby_legal_aid(lat, lon)
    for place in places:
        tags = place.get("tags", {})
        name = tags.get("name", "Unnamed")
        place_type = tags.get("amenity") or tags.get("office", "Legal Aid")
        icon_color = "green" if place_type == "lawyer" else "blue"
        folium.Marker(
            location=[place["lat"], place["lon"]],
            popup=f"{name} ({place_type})",
            icon=folium.Icon(color=icon_color)
        ).add_to(m)

    st_folium(m, width=700, height=500)

    if not places:
        st.info("ℹ️ No legal aid locations found nearby.")

if city:
    with st.spinner("🗺️ Loading map and fetching nearby legal aid..."):
        show_osm_map(city)

# -------------------------------
# ✅ GENAI INSIGHTS
# -------------------------------
def analyze_response_insights(user_query, ai_response):
    prompt = f"""
    Analyze the following user query and AI response. Identify:
    1. Intent of the user query
    2. Key takeaways from the AI response
    3. If any, suggest follow-up actions the user should consider.

    User Query:
    {user_query}

    AI Response:
    {ai_response}

    Provide the result as:
    - **Intent:** ...
    - **Key Takeaways:**
      - ...
      - ...
    - **Suggested Actions:**
      - ...
    """
    return generate_response(prompt)

st.markdown("---")
st.subheader("📊 AI Insights on Your Query")

if query and 'summarized_response' in locals():
    try:
        with st.spinner("🧠 Analyzing insights from response..."):
            insights = analyze_response_insights(query, summarized_response)
            st.markdown(insights)
    except Exception as e:
        st.warning(f"⚠️ Could not generate insights: {e}")
