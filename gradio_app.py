import os
import logging
from dotenv import load_dotenv
import gradio as gr

from brain_of_the_doctor import encoded_image, analyz_image_with_query
from voice_of_the_patient import record_audio, audio_to_text
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

def setup_logging():
    log_file = os.getenv("LOG_FILE", "ai_doctor.log")
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="a"),
            logging.StreamHandler()
        ]
    )

SYSTEM_PROMPT = (
    "You have to act as a professional doctor, I know you are not but this is for learning purpose. "
    "What’s in this image? Do you find anything wrong with it medically? "
    "If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in "
    "your response. Your response should be in one long paragraph. Also always answer as if you are answering to "
    "a real person. Do not say ‘In the image I see’ but say ‘With what I see, I think you have ….‘ "
    "Do not respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, "
    "Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"
)

load_dotenv()
setup_logging()


def process_inputs(audio_file_path: str, image_path: str):
    logging.debug("--- New request received ---")
    logging.debug(f"Audio file path: {audio_file_path}")
    logging.debug(f"Image file path: {image_path}")

    try:
        speech_to_text_output = audio_to_text(
            GROQ_API_KEY=os.getenv("GROQ_API_KEY"),
            audio_file_path=audio_file_path,
            stt_model="whisper-large-v3"
        )
        logging.debug(f"Speech-to-text output: {speech_to_text_output}")
    except Exception as e:
        logging.error(f"Error during speech-to-text: {e}")
        speech_to_text_output = ""

    if image_path:
        full_prompt = SYSTEM_PROMPT + " " + speech_to_text_output
        logging.debug(f"Full LLM query: {full_prompt}")

        try:
            doctor_response = analyz_image_with_query(
                query=full_prompt,
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                encoded_image=encoded_image(image_path)
            )
            logging.debug(f"Doctor response from LLM: {doctor_response}")
        except Exception as e:
            logging.error(f"Error during image analysis: {e}")
            doctor_response = "Sorry, there was an error analyzing the image."
    else:
        doctor_response = "No image provided for me to analyze."
        logging.debug("No image path provided; skipping image analysis.")

    try:
        voice_of_doctor_path = "final.mp3"
        text_to_speech_with_gtts(
            input_text=doctor_response,
            output_file_path=voice_of_doctor_path
        )
        logging.debug(f"Generated speech file at: {voice_of_doctor_path}")
    except Exception as e:
        logging.error(f"Error during text-to-speech: {e}")
        voice_of_doctor_path = None

    logging.debug("--- Request processing complete ---\n")
    return speech_to_text_output, doctor_response, voice_of_doctor_path

def main():
    inface = gr.Interface(
        fn=process_inputs,
        inputs=[
            gr.Audio(sources=["microphone"], type="filepath"),
            gr.Image(type="filepath")
        ],
        outputs=[
            gr.Textbox(label="Speech to Text"),
            gr.Textbox(label="Doctor's Response"),
            gr.Audio(label="Doctor's Voice")
        ],
        title="AI Doctor with Vision and Voice",
        description="Upload an image and ask your medical question verbally.",
        allow_flagging="never"
    )

    inface.launch()

if __name__ == "__main__":
    main()