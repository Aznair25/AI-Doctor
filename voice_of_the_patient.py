#step 1:set up audio recorder(ffmped and portaudio)
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path,timeout=20,pharase_time_limit=None):
    """
    SImplified function to record audio from microphone and save it as MP3 file.

    Args:
    file_path (str): Path to save recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    pharase_time_limit (int): Maximum time for the pharase to be recoded (in seconds).
    """
    recognizer=sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for Ambient Noice.....")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking Now.....")

            #record audio
            audio_data=recognizer.listen(source,timeout=timeout,pharase_time_limit=pharase_time_limit)
            logging.info("Recording Complete......")
            #convert the recorded audio to mp3 file
            wav_data=audio_data.get_wav_data()
            audio_segment=AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path,format="mp3",bitrate='128k')

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occured: {e}")
   

#step 2: Set up speech to text-SST-model for transcription
import os 
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
stt_model="whisper-large-v3"

def audio_to_text(GROQ_API_KEY,audio_file_path,stt_model):
    client=Groq(api_key=GROQ_API_KEY)
    
    audio_file=open(audio_file_path,"rb")
    transcription=client.audio.transcriptions.create(
        model=stt_model,
        file=audio_file,
        language="en"
    )
    return transcription.text


# if __name__=="__main__":
#     audio_file_path="voice_of_the_patient.mp3"
#     record_audio(file_path=audio_file_path) 