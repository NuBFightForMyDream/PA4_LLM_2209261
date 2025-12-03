import google.generativeai as genai
import os

# --- 1. ตั้งค่า API Key ---
# แนะนำให้ใส่ Key ตรงนี้ หรือดึงจาก Environment Variable
# genai.configure(api_key="YOUR_API_KEY_HERE")
# เพื่อความปลอดภัย ผมสมมติว่าคุณ set env variable แล้ว หรือใส่ string ตรงๆ เพื่อเทสก่อนก็ได้ครับ
API_KEY = "ใส่_API_KEY_ของคุณตรงนี้" 
genai.configure(api_key=API_KEY)

def generate_novel_idea_from_lyrics(song_name, artist, lyrics):
    """
    ฟังก์ชันรับเนื้อเพลง แล้วยิงไปหา AI เพื่อขอพล็อตนิยาย
    """
    
    # เลือกโมเดล (Gemini 1.5 Flash เร็วและประหยัด เหมาะกับงาน Text)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # --- 2. สร้าง Prompt (คำสั่ง) ---
    # นี่คือส่วนที่สำคัญที่สุด เปรียบเสมือนการบรีฟงานนักเขียน
    prompt_template = f"""
    Role: คุณคือนักเขียนนิยายมืออาชีพและนักวิเคราะห์ดนตรี
    Task: วิเคราะห์เนื้อเพลงด้านล่างนี้ แล้วเปลี่ยนให้เป็น "โครงเรื่องนิยาย (Novel Plot)" ที่น่าสนใจ
    
    ข้อมูลเพลง:
    - เพลง: {song_name}
    - ศิลปิน: {artist}
    - เนื้อเพลง: 
    "{lyrics}"

    Requirement (สิ่งที่ต้องตอบกลับมา):
    1. **Mood & Tone**: อารมณ์หลักของเรื่อง (เช่น เหงาจับใจ, รักโรแมนติกสดใส, ลึกลับซ่อนเงื่อน)
    2. **Genre**: แนวของนิยาย (เช่น Coming of Age, Thriller, Romantic Drama)
    3. **Character Concept**: ออกแบบตัวละครเอก 2 คน (พระเอก/นางเอก หรือ ตัวดำเนินเรื่อง) ที่สะท้อนบุคลิกจากเพลง
    4. **Setting**: ฉากหลังของเรื่องที่เข้ากับบรรยากาศเพลง
    5. **Story Outline (เรื่องย่อ)**:
       - จุดเริ่มต้น (Intro): เหตุการณ์ที่ทำให้ตัวละครมาเจอกัน หรือเกิดปัญหา
       - จุดพีค (Climax): เหตุการณ์สำคัญที่สุดที่บีบคั้นอารมณ์ตามท่อนฮุคของเพลง
       - ตอนจบ (Ending): บทสรุปของความสัมพันธ์
    
    หมายเหตุ: ขอภาษาไทยที่สละสลวย อ่านแล้วเห็นภาพ
    """

    # --- 3. ส่งคำสั่งไปหา AI ---
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