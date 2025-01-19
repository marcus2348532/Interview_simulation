import streamlit as st
from PyPDF2 import PdfReader
import pdfplumber
from streamlit_extras.switch_page_button import switch_page
import toml
import os
import streamlit as st

st.set_page_config(
    page_title="Resume Upload",
    page_icon="📈",
    layout="wide",  
    initial_sidebar_state="collapsed") 
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
st.sidebar.success("Select page above")

def read_pdf(file):
    reader=PdfReader(file)
    count=len(reader.pages)
    all_page_text=""
    for i in range(count):
        page=reader.pages[i]
        all_page_text+=page.extract_text()
    return all_page_text


text=''
def main():
    st.title("RESUME UPLOAD") 
    file=st.file_uploader("Upload resume",type=["pdf"])
    if st.button("Process"):
        if file is not None:
            #filename=file.nameupload 
            #filesize=file.size
            #st.write(filename,filesize)
            text=read_pdf(file)
            #st.write(text)
            st.session_state.resume_details= text

            

            st.switch_page("pages\interview_type.py")

if __name__=='__main__':
    main()

    