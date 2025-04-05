from brain_of_the_doctor import encoded_image,analyz_image_with_query
from voice_of_the_patient import record_audio, audio_to_text
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs
import os
from dotenv import load_dotenv
import gradio as gr


system_prompt = """You have to act as a professional doctor, I know you are not but this is for learning purpose.
What’s in this image? Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to
a real person.
Do not say ‘In the image I see’ but say ‘With what I see, I think you have ….’
Do not respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot,
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_file_path,image_path):
    load_dotenv()
    speech_to_text_output=audio_to_text(
        GROQ_API_KEY=os.getenv("GROQ_API_KEY"),
        audio_file_path=audio_file_path,
        stt_model="whisper-large-v3"
    )

    if image_path:
        doctor_response=analyz_image_with_query(
            query=system_prompt+speech_to_text_output,
            model="llama-3.2-90b-vision-preview",
            encoded_image=encoded_image(image_path)
        )
        
    else:
        doctor_response="No image provided for me to analyze."
    
    voice_of_doctor=text_to_speech_with_gtts(
        input_txet=doctor_response,
        output_file_path="final.mp3"
    )

    return speech_to_text_output,doctor_response,voice_of_doctor

#create the interface
inface=gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"],type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Doctor with Vision and Voice"
)

inface.launch(debug=True)