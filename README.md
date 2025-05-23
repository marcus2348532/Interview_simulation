# Interview_simulation
Interview Simulation Using LLM

This is an Interview Simulation App built using Streamlit, Google Speech-to-Text, and Langchain for conversational AI. The app allows users to record answers to interview questions, transcribe them using Google's Speech-to-Text API, and generate lip-synced videos of the avatar asking the next question. The avatar and conversation flow are powered by Langchain and Groq's AI model.

Requirements :

Python 3.8+ Streamlit SpeechRecognition Langchain requests toml langchain_groq (for using Groq-powered AI) Google Speech-to-Text API Key Groq API Key (for generating AI responses)

Working :

Start Interview: The user is prompted to upload a resume. The AI generates questions based on the resume and interview type. The first question is presented along with a video of the avatar asking the question.

Record Answers: The user clicks a button to record their answer to the question. After the user finishes recording, the speech is transcribed to text using Google Speech-to-Text.

Process Answer and Generate Video: The text is processed using Langchain to generate the next question. A lip-synced video is generated of the avatar asking the next question.

Repeat for Multiple Questions: The process continues for a specified number of questions (default is 5).

Evaluate: The interview is evaluated after all questions are answered, and feedback is provided based on the responses.

API Integration :

Google Speech-to-Text:The app uses Google's Speech-to-Text API for transcribing the user's voice into text. For the API to work, you need to provide your own credentials. 2.Groq API :Groq provides conversational AI capabilities, which are used for generating interview questions based on the user's resume. The API is called when fetching responses during the interview.
