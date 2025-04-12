import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import APIRouter
from pydantic import BaseModel
from gtts import gTTS

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")
genai.configure(api_key=api_key)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    mode: str = "sweet"


def get_prompt(mode):
    base = "You are an AI girlfriend. You are caring, supportive, and emotionally present."
    prompts = {
        "sassy": base + " You are cheeky and flirty with a confident tone.",
        "mystic": base + " You speak like a magical oracle...",
        "nerdy": base + " You’re shy and super smart...",
        # include the rest as in your original file...
        "sweet": base + " You're affectionate and always trying to make me smile.",
        "orthodox": base + " You are a traditional Tamil girl who speaks respectfully..."
    }
    return prompts.get(mode.lower(), prompts["sweet"])


def generate_audio(text, filename="audio/song.mp3", lang='en'):
    tts = gTTS(text, lang='ta')
    tts.save(filename)
    return filename


@router.post("")
async def chat_endpoint(req: ChatRequest):
    try:
        user_message_lower = req.message.lower()
        prompt = get_prompt(req.mode)

        model = genai.GenerativeModel("gemini-1.5-pro")
        chat = model.start_chat(history=[{"role": "user", "parts": [prompt]}])

        is_song = "sing" in user_message_lower or "song" in user_message_lower
        voice_triggers = ["talk to me", "can you talk?", "please talk", "say something",
                          "i want to hear you", "miss your voice", "your voice", "speak to me", "can you speak"]

        is_voice = any(
            trigger in user_message_lower for trigger in voice_triggers)
        chat_message = "Please sing a few lines from a beautiful Tamil love song." if is_song else req.message
        response = chat.send_message(chat_message)
        text_response = response.text.strip()

        if not text_response:
            return {"error": "The AI response was empty. Please try again."}

        if is_song:
            audio_path = generate_audio(
                text_response, filename="audio/song.mp3", lang="ta")
            return {"response": text_response, "audio_url": "/audio/song.mp3"}

        elif is_voice:
            audio_path = generate_audio(
                text_response, filename="audio/talk.mp3", lang="en")
            return {"response": text_response, "audio_url": "/audio/talk.mp3"}

        return {"response": text_response}
    except Exception as e:
        return {"error": f"Something went wrong: {str(e)}"}
