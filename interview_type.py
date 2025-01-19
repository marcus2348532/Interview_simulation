import streamlit as st
import toml
import os
import streamlit as st
st.set_page_config(
    page_title="My App",
    page_icon="📈",
    layout="wide",  # You can set this to 'centered' if you prefer
    initial_sidebar_state="collapsed"  # Collapse the sidebar by default
)

# Define the path for the .streamlit/config.toml file
config_dir = os.path.join(os.getcwd(), '.streamlit')
os.makedirs(config_dir, exist_ok=True)
config_path = os.path.join(config_dir, 'config.toml')

# Define the theme settings
config = {
    "theme": {
        "primaryColor": "#FFFFFF",
        "backgroundColor": "#000000",
        "secondaryBackgroundColor": "#333333",
        "textColor": "#FFFFFF",
        "font": "sans serif"
    }
}

# Write the configuration to the config.toml file
with open(config_path, 'w') as config_file:
    toml.dump(config, config_file)

print(f"Streamlit configuration written to {config_path}")

# Set the sidebar state and other page configurations in your Streamlit script


interview_types = [
    "Technical",
    "Behavioral",
    "HR"
]

# Create the title and selection boxes
st.title("Select Interview Type")

selected_interview_type = st.selectbox("Select Interview Type", interview_types)


# Proceed button logic
if st.button("Proceed"):
    st.session_state['interview_type'] = selected_interview_type
    st.session_state['page'] = "interview"
    
# Redirect to the interview page if the page state is set to "interview"
if 'page' in st.session_state and st.session_state['page'] == "interview":
    st.switch_page("pages\Video_full_display.py")
