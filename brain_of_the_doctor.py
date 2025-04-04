#step 1: set up GROQ API KEY
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=".env")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
# print("Load API Key:",GROQ_API_KEY)


#step 2: convert the image to required format
import base64
image_path=r"F:\Bot\image.png"
image_file=open(image_path,"rb")
encoded_image=base64.b64encode(image_file.read()).decode("utf_8")

#step 3: set up multimodal llm
from groq import Groq
client=Groq()
query="What is the issue with my skin?"
model="llama-3.2-90b-vision-preview"
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
print(chat_completion.choices[0].message.content)