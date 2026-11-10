import streamlit as st
import asyncio
import os
import yt_dlp
import whisper

# --- PIL Compatibility Fix for MoviePy ---
from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS
# -----------------------------------------

from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.video.fx.all as vfx

st.set_page_config(page_title="A to Z Movie Recap Studio (Stable)", page_icon="🎬", layout="centered")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    .main-title {
        font-size: 28px;
        font-weight: bold;
        color: #111;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 14px;
        color: #666;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Top Bar Header
st.markdown('<p class="main-title">🎬 A to Z Movie Recap Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">100% Error Free & Copyright Safe - အကောင်းဆုံး Recap များကို ဖန်တီးပါ</p>', unsafe_allow_html=True)
st.markdown("---")

# Session State Initialization
if 'extracted_script' not in st.session_state:
    st.session_state['extracted_script'] = ""
if 'last_youtube_url' not in st.session_state:
    st.session_state['last_youtube_url'] = ""

video_file_path = "source_movie.mp4"

# ==========================================
# Step 1: Source Selection
# ==========================================
st.markdown("### 01. Source ကို ရွေးပါ (TikTok များအတွက် ဖိုင်တင်ပါ)")
input_method = st.radio("📂 ဗီဒီယိုရယူမည့် နည်းလမ်း", ["ကွန်ပျူတာထဲမှ ဖိုင်တင်မည် (အကောင်းဆုံးနှင့် အသေချာဆုံး)", "YouTube/Social Link ဖြင့် ဒေါင်းလုဒ်ဆွဲမည်"])

if "ကွန်ပျူတာ" in input_method:
    uploaded_file = st.file_uploader("📤 SnapTik (သို့) အခြားမှ ဒေါင်းထားသော ဗီဒီယိုဖိုင်ကို တင်ပါ", type=["mp4", "mov", "avi"])
    if uploaded_file is not None:
        with open(video_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ ဗီဒီယိုဖိုင် တင်ပြီးပါပြီ! အောက်ပါအဆင့်များကို ဆက်လုပ်နိုင်ပါပြီ။")
else:
    social_url = st.text_input("🔗 Video Link ထည့်ရန်", placeholder="https://www.youtube.com/...")
    if social_url != st.session_state['last_youtube_url']:
        st.session_state['extracted_script'] = ""
        st.session_state['last_youtube_url'] = social_url

    if social_url and st.button("📥 ဗီဒီယို ဒေါင်းလုဒ်ဆွဲမည်"):
        with st.spinner("⏳ ဒေါင်းလုဒ်ဆွဲနေပါပြီ..."):
            try:
                if os.path.exists(video_file_path):
                    os.remove(video_file_path)
                ydl_opts = {'format': 'bv*+ba/b', 'outtmpl': video_file_path, 'merge_output_format': 'mp4'}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([social_url])
                st.success("🎉 ဒေါင်းလုဒ်ပြီးပါပြီ!")
            except Exception as e:
                st.error(f"❌ Error: {e} (TikTok link များအတွက် ဖိုင်ဒေါင်းပြီး တိုက်ရိုက်တင်ပါ။)")

st.markdown("---")

# ==========================================
# Step 2: Settings, Copyright Tools & AI Transcript
# ==========================================
st.markdown("### 02. Video Setting, Copyright Tools & AI Transcript")

col1, col2, col3 = st.columns(3)
with col1:
    target_ratio = st.selectbox("📐 Video Frame", ["9:16 (TikTok/Reels)", "16:9 (YouTube/FB)"])
with col2:
    voice_gender = st.selectbox("🎙️ အသံ", ["female (Nilar)", "male (Thiha)"])
with col3:
    dialogue_speed = st.slider("🗣️ Speed Play", 0.9, 2.0, 1.2, 0.1)

st.markdown("🛡️ **Copyright Protection Tools**")
enable_mirror = st.checkbox("🔄 Video Mirroring (ဘယ်ညာလှည့်မည်)", value=True)
enable_color_filter = st.checkbox("🎨 Color Adjustment (အရောင်ပြောင်းမည်)", value=True)

if os.path.exists(video_file_path):
    if st.button("🎙️ AI ဖြင့် အသံထုတ်မည် (တရုတ်/ကိုရီးယား လာလျှင် အင်္ဂလိပ်လို တိုက်ရိုက်ထွက်ပါမည်)"):
        with st.spinner("⏳ Whisper ဖြင့် စာသားထုတ်ယူနေပါပြီ... ခဏစောင့်ပါ..."):
            try:
                model = whisper.load_model("base")
                result = model.transcribe(video_file_path, task="translate")
                st.session_state['extracted_script'] = f"--- မူရင်းအင်္ဂလိပ်ဘာသာပြန် (ဤနေရာတွင် မြန်မာလို အစားထိုးရေးပါ) ---\n\n{result['text']}"
                st.success("🎉 စာသားထုတ်ယူပြီးပါပြီ။")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")

script_text = st.text_area("📜 Recap Script (ဤနေရာတွင် မြန်မာလို အစားထိုး ပြင်ဆင်ရေးသားပါ)", value=st.session_state['extracted_script'], height=220)
if script_text != st.session_state['extracted_script']:
    st.session_state['extracted_script'] = script_text

st.markdown("---")

# ==========================================
# Step 3: Render & Download
# ==========================================
st.markdown("### 03. Sync & Download လုပ်ပါ")

if st.button("🚀 ဗီဒီယိုနှင့်အသံ ချိန်ညှိထုတ်လုပ်မည် (Render Video)"):
    if not os.path.exists(video_file_path) or not st.session_state['extracted_script']:
        st.warning("⚠️ ဗီဒီယိုဖိုင်နှင့် ဇာတ်လမ်းစာသား အပြည့်အစုံ လိုအပ်ပါသည်။")
    else:
        with st.spinner("⏳ ဖန်တီးနေပါပြီ (Edge-TTS & MoviePy Syncing)... ခဏစောင့်ပါ..."):
            try:
                import edge_tts
                selected_voice = "my-MM-NilarNeural" if "female" in voice_gender else "my-MM-ThihaNeural"
                
                rate_percentage = int((dialogue_speed - 1.0) * 100)
                rate_str = f"+{rate_percentage}%" if rate_percentage >= 0 else f"{rate_percentage}%"
                
                async def generate_audio():
                    communicate = edge_tts.Communicate(st.session_state['extracted_script'].strip(), selected_voice, rate=rate_str)
                    await communicate.save("temp_voice.mp3")
                asyncio.run(generate_audio())
                
                video = VideoFileClip(video_file_path)
                audio = AudioFileClip("temp_voice.mp3")
                
                # Frame ချိန်ညှိခြင်း
                w, h = video.size
                if "9:16" in target_ratio:
                    new_w = int(h * 9 / 16)
                    x_center = w / 2
                    video = video.crop(x1=x_center - new_w/2, y1=0, x2=x_center + new_w/2, y2=h)
                    video = video.resize(height=1280)
                else:
                    video = video.resize(width=1280)
                
                # Copyright Effects
                if enable_mirror:
                    video = video.fx(vfx.mirror_x)
                if enable_color_filter:
                    video = video.fx(vfx.colorx, 1.05)
                
                # Syncing
                processed_video = video.fx(vfx.speedx, dialogue_speed)
                target_duration = audio.duration
                
                if processed_video.duration > target_duration:
                    processed_video = processed_video.subclip(0, target_duration)
                elif processed_video.duration < target_duration:
                    processed_video = processed_video.set_duration(target_duration)
                
                final_video = processed_video.set_audio(audio)
                output_filename = "Final_AZ_Master_Recap.mp4"
                
                final_video.write_videofile(output_filename, codec="libx264", audio_codec="aac", fps=24, preset="ultrafast", threads=4)
                
                st.success("🎉 အောင်မြင်စွာ ပြီးဆုံးပါပြီ!")
                st.video(output_filename)
                
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="📥 Master ဗီဒီယိုကို Download ဆွဲရန်",
                        data=file,
                        file_name="AZ_Master_Movie_Recap.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"❌ Error: {e}")