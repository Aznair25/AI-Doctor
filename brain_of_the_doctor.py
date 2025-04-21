#step 1: set up GROQ API KEY
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=".env")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")


#step 2: convert the image to required format
import base64
image_path=r"F:\Bot\image.png"
def encoded_image(image_path):
    image_file=open(image_path,"rb")
    return base64.b64encode(image_file.read()).decode("utf_8")

#step 3: set up multimodal llm

from groq import Groq

query="What is the issue with my skin?"
model="meta-llama/llama-4-scout-17b-16e-instruct"

def analyz_image_with_query(query,model,encoded_image):
    client=Groq()

    messages=[
        {
            "role":"user",
            "content":[
                {
                    "type":"text",
                    "text":query
                },
                {
                    "type":"image_url",
                    "image_url":{
                        "url": f"data:image/png;base64,{encoded_image}"
                    },
                },
            ],
        }
    ]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )
    return chat_completion.choices[0].message.content
