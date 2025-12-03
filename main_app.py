import google.generativeai as genai
import os
import streamlit as st

# --- 1. ตั้งค่า API Key ---
# แนะนำให้ใส่ Key ตรงนี้ หรือดึงจาก Environment Variable
# genai.configure(api_key="YOUR_API_KEY_HERE")
# เพื่อความปลอดภัย ผมสมมติว่าคุณ set env variable แล้ว หรือใส่ string ตรงๆ เพื่อเทสก่อนก็ได้ครับ
API_KEY = "ใส่_API_KEY_ของคุณตรงนี้" 
genai.configure(api_key=API_KEY)

def generate_novel_idea_from_lyrics(song_name, artist, lyrics, api_key=None):
    """
    ฟังก์ชันรับเนื้อเพลง แล้วยิงไปหา AI เพื่อขอพล็อตนิยาย
    """
    if api_key:
        genai.configure(api_key=api_key)
    else:
        # ถ้าไม่มีในพาราม ส่งให้ใช้จาก env ถ้ามี
        env_key = os.getenv("GENAI_API_KEY") or os.getenv("API_KEY")
        if env_key:
            genai.configure(api_key=env_key)

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt_template = f"""
    Role: คุณคือนักเขียนนิยายมืออาชีพและนักวิเคราะห์ดนตรี
    Task: วิเคราะห์เนื้อเพลงด้านล่างนี้ แล้วเปลี่ยนให้เป็น "โครงเรื่องนิยาย (Novel Plot)" ที่น่าสนใจ

    ข้อมูลเพลง:
    - เพลง: {song_name}
    - ศิลปิน: {artist}
    - เนื้อเพลง:
    "{lyrics}"

    Requirement (สิ่งที่ต้องตอบกลับมา):
    1. Mood & Tone: อารมณ์หลักของเรื่อง
    2. Genre: แนวของนิยาย
    3. Character Concept: ออกแบบตัวละครเอก 2 คน
    4. Setting: ฉากหลังของเรื่อง
    5. Story Outline (เรื่องย่อ):
       - จุดเริ่มต้น (Intro)
       - จุดพีค (Climax)
       - ตอนจบ (Ending)

    ขอเป็นภาษาไทยที่สละสลวย อ่านแล้วเห็นภาพ
    """

    try:
        response = model.generate_content(prompt_template)
        return response.text
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"

# --- ส่วนทดสอบการทำงาน (Main) ---
if __name__ == "__main__":
    # สมมติเพลง "ทิ้งไว้กลางทาง" - Potato (ตัวอย่างสั้นๆ)
    test_song = "ทิ้งไว้กลางทาง"
    test_artist = "Potato"
    test_lyrics = """
    มันจบแล้ว กลั้นน้ำตาไว้ไม่ไหว
    ขีดจำกัดจะอดทนได้แค่ไหน
    ถึงรักมากเท่าไหร่ ก็ต้องตัดใจปล่อยเธอไปอยู่ดี
    สุดท้ายความรักไม่ช่วยอะไรเลย
    """
    
    print(f"กำลังวิเคราะห์เพลง: {test_song}...")
    result = generate_novel_idea_from_lyrics(test_song, test_artist, test_lyrics)
    
    print("-" * 40)
    print(result)
    print("-" * 40)

# Streamlit UI
st.set_page_config(page_title="Novel Plot from Lyrics", layout="wide")
st.title("สร้างโครงเรื่องนิยายจากเนื้อเพลง")
st.caption("ป้อนชื่อเพลง, ศิลปิน และเนื้อเพลง แล้วกด Generate")

with st.sidebar:
    st.header("การตั้งค่า")
    api_key_input = st.text_input("API Key (ถ้ามี)", type="password")
    use_env = st.checkbox("ใช้ API Key จาก environment (GENAI_API_KEY / API_KEY)", value=True)
    st.write("หากกรอก API Key ในช่องข้างบน จะใช้ค่านั้นแทน env")

song_name = st.text_input("ชื่อเพลง", value="ทิ้งไว้กลางทาง")
artist = st.text_input("ศิลปิน", value="Potato")
lyrics = st.text_area("เนื้อเพลง", value="""มันจบแล้ว กลั้นน้ำตาไว้ไม่ไหว
ขีดจำกัดจะอดทนได้แค่ไหน
ถึงรักมากเท่าไหร่ ก็ต้องตัดใจปล่อยเธอไปอยู่ดี
สุดท้ายความรักไม่ช่วยอะไรเลย""", height=200)

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("Generate"):
        key_to_use = None
        if api_key_input:
            key_to_use = api_key_input
        elif use_env:
            key_to_use = os.getenv("GENAI_API_KEY") or os.getenv("API_KEY")

        with st.spinner("กำลังติดต่อโมเดลและสร้างโครงเรื่อง..."):
            result_text = generate_novel_idea_from_lyrics(song_name, artist, lyrics, api_key=key_to_use)
            st.session_state["last_result"] = result_text
with col2:
    st.subheader("ผลลัพธ์")
    last = st.session_state.get("last_result", "")
    if last:
        st.markdown(last)
    else:
        st.info("ยังไม่มีผลลัพธ์ — กด Generate เพื่อเริ่ม")

if st.button("ตัวอย่าง (เติมค่าและ Generate)"):
    # ปุ่มนี้เพื่อช่วยทดสอบ โดยเติมค่าเริ่มต้นแล้วกด Generate
    st.experimental_rerun()