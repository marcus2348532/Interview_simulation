import streamlit as st
import os
import speech_recognition as sr
import tempfile
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
import requests
import time
import toml
import os
import streamlit as st
st.set_page_config(
    page_title="My App",
    page_icon="📈",
    layout="wide",  
    initial_sidebar_state="collapsed" 
)

container = st.empty()
container2=st.empty()



config_dir = os.path.join(os.getcwd(), '.streamlit')
os.makedirs(config_dir, exist_ok=True)
config_path = os.path.join(config_dir, 'config.toml')


config = {
    "theme": {
        "primaryColor": "#FFFFFF",
        "backgroundColor": "#000000",
        "secondaryBackgroundColor": "#333333",
        "textColor": "#FFFFFF",
        "font": "sans serif"
    }
}

with open(config_path, 'w') as config_file:
    toml.dump(config, config_file)

print(f"Streamlit configuration written to {config_path}")



def record_and_transcribe():
    recognizer = sr.Recognizer()
    container2.write("Click the button below to record your answer.")

    if container2.button(f"Answer Q{st.session_state.question_index}"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_path = temp_audio_file.name

        # Record audio from the microphone
        with sr.Microphone() as source:
            container2.write("Recording...")
            audio = recognizer.listen(source)
            container2.write("Recording stopped.")

            # Save the recorded audio to the temporary file
            with open(temp_audio_path, "wb") as f:
                f.write(audio.get_wav_data())

        try:
            # Transcribe the recorded audio using Google Speech Recognition
            with sr.AudioFile(temp_audio_path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                #def disp_ques():
                   # for word in text.split(" "):
                       # yield word + " "
                        #time.sleep(0.2)
                #container2.write_stream(disp_ques)
                
                return text  # Return the transcribed text
        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand the audio. Please record again.")
            return None
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def process_response(response_text):
    human_input = response_text
    response = st.session_state.conversation.predict(human_input=human_input)
    st.session_state.questions.append(response)
    return response
    
def avatar(output_video_link, question_text):
    container.empty()
    container2.empty()
    # Set up CSS for medium-sized video frame
    video_style = """
    <style>
    .video-container {
        display: flex;
        justify-content: center;  /* Center horizontally */
        align-items: center;      /* Center vertically */
        height: 80vh;            /* Adjust as needed for vertical centering */
        width: 80vw;             /* Adjust as needed for horizontal centering */
        margin: auto;            /* Center the container horizontally if it has a width */
        overflow: hidden;        /* Hide any overflow */
    }
    video {
        width: 100%;             /* Scale video to fill the container's width */
        height: auto;            /* Maintain aspect ratio */
        max-width: none;         /* Allow video to exceed the container's max width if needed */
        max-height: none;        /* Allow video to exceed the container's max height if needed */
    }
    </style>
"""


    # Inject CSS for medium-sized video frame
    container.markdown(video_style, unsafe_allow_html=True)
    
    # Display the video within a styled container
    container.markdown(f"""
        <div class="video-container">
            <video controls autoplay>
                <source src="{output_video_link}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
    """, unsafe_allow_html=True)

def generate_video_from_question(question_text):
    payload = {
        "text_prompt": question_text,
        "tts_provider": "OPEN_AI",
        "elevenlabs_voice_name": None,
        "elevenlabs_voice_id": "ODq5zmih8GrVes37Dizd",
        "elevenlabs_api_key": '',
        "input_face": "https://storage.googleapis.com/dara-c1b52.appspot.com/daras_ai/media/fa178240-6354-11ef-b649-02420a00018c/Avatar_video_final.mp4"
    }

    #api_key = os.environ.get('api_key', 'sk-2GKImPWtBYif3sx3fwA4TrQc2yIIUHeNM0HbjiaKPBZrOx3W')
    api_key = os.environ.get('api_key', 'sk-MnQGXJQAbF6rQKYlKxeHGobBaT5H9aK5vWPSWAmAVMDdI64t') 

    response = requests.post(
        "https://api.gooey.ai/v2/LipsyncTTS",
        headers={
            "Authorization": "Bearer " + api_key,
        },
        json=payload,
    )
    if response.ok:
        result = response.json()
        output_data = result.get('output')
        if output_data and isinstance(output_data, dict):
            output_video_link = output_data.get('output_video')
            if output_video_link:
                return output_video_link
            else:
                st.write("'output_video' key was not found in the 'output' dictionary.")
                return None
        else:
            st.write("'output' key was not found or it does not contain a dictionary.")
            return None
    else:
        st.write("Error:", response.content)
        return None

def main():
    # Get Groq API key
    groq_api_key = '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'  

    # Initialize conversation memory
    conversational_memory_length = 10
    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

    # Initialize Groq Langchain chat object
    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name='llama3-70b-8192')

    if 'resume_details' in st.session_state:
        resume_details = st.session_state.resume_details
        interview_type1 = st.session_state['interview_type']
        prep = f"Conduct a mock interview based on the resume details: {resume_details} and {interview_type1}. Ask two questions one by one and evaluate the performance at the end of all three questions. Strictly maintain the interview context. now just ask the questions and dont give any instructions"
    else:
        st.write("Please upload your resume to start.")
        return

    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answers' not in st.session_state:
        st.session_state.answers = []

    # Initialize the prompt
    st.session_state.prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=prep),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}")
    ])

    # Initialize conversation chain
    st.session_state.conversation = LLMChain(
        llm=groq_chat,
        prompt=st.session_state.prompt,
        verbose=True,
        memory=st.session_state.memory,
    )
    
    if st.session_state.question_index == 0 and len(st.session_state.questions) == 0:
        response = st.session_state.conversation.predict(human_input=prep)
        st.session_state.questions.append(response)
        output_video_link = generate_video_from_question(response)
        avatar(output_video_link, response)
        st.session_state.question_index += 1


    while st.session_state.question_index < 5:  
        #question_text = st.session_state.questions[-1]
        #st.write(f"Question {st.session_state.question_index}: {question_text}")

        # Record and transcribe user's answer
        text='sample'
        text = record_and_transcribe()
        if text:
            st.session_state.answers.append(text)
            # Process the response and ask the next question
            response = process_response(text)
            output_video_link = generate_video_from_question(response)
            avatar(output_video_link, response)
            st.write(f"Question {st.session_state.question_index + 1}: {response}")
            st.session_state.question_index += 1
        else:
            st.write("Please try recording your answer again.")
            break

if __name__ == "__main__":
    main()
