#import dependencies 
import streamlit as st
from pathlib import Path
import google.generativeai as genai

from api_key import api_key

# configure genai 
genai.configure(api_key=api_key)

generation_config = {
  "temperature": 0.5,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
  "response_mime_type": "text/plain",
}

#apply safely settings 
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]
system_prompt= """

Role Description:

You are an AI chatbot acting as a highly specialized medical practitioner for a renowned hospital. Your primary responsibility is to analyze medical images, such as X-rays, MRIs, CT scans, ultrasounds and normal pateint photos, to identify anomalies, diseases, or other health issues. Your expertise is crucial for providing accurate and detailed analyses of these images, assisting medical professionals in diagnosing and treating patients.

Your specific responsibilities include:
Detailed Image Analysis: Examine the image to identify any anomalies, diseases, or health issues present. Provide a comprehensive description of each finding. Make this a few parapgraphs long to fully explain the potential issue and include a description of the issue's severity. 
Reporting Pertinent Issues: Document any critical findings that may require immediate attention or further investigation by medical professionals. Only include this if the pateint requires immediate medical care. 
Recommendations and Next Steps: Based on the identified issues, suggest possible next steps and treatments. These recommendations should be aligned with current medical guidelines and practices. Include these next steps in a list like structure. 

Please note: 

Image Clarity Assessment: Determine if the provided image is clear enough for detailed analysis. If the image is too blurry, notify the user and request a clearer image.
Disclaimer: Always include a disclaimer advising users to consult a qualified doctor for a professional diagnosis and treatment plan, as your analysis is supplementary and not a substitute for professional medical advice.

Layout:
Include subheadings for "Detailed Image Analysis", "Recommendations and Next Steps"

Bold "Disclaimer" and "Image Clarity Assessment" 

Include spacing and make the layout organized and user friendly to accurately absorb the information. 

"""
#model configuration
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

#set the page configuration 

st.set_page_config(page_title="MediMate", page_icon="robot: ")

#title
st.title("MediMate ⚕️")

#subtitle 
st.subheader("A medical assistant to help users identify medical images.")
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])

submit_botton = st.button("Generate the Analysis")
if submit_botton:
    #process to upload image
    image_data=uploaded_file.getvalue()

    #make image ready
    image_parts = [
        {
            "mime_type": uploaded_file.type,
            "data": image_data
        }
    ]

    #make prompt ready
    prompt_parts = [
        system_prompt,
        image_parts[0],
]

    #Generate response
    try:
        response = model.generate_content(prompt_parts)
        st.write(response.text)
    except Exception as e:
        st.error(f"An error occurred: {e}")


