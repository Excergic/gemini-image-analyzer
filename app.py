from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI API (Gemini)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini Pro Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get the Gemini AI response
def get_gemini_response(input, image):
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text
    

# Set Streamlit page configuration for a better UI
st.set_page_config(page_title="Gemini AI Image & Text Analyzer", layout="wide", initial_sidebar_state="expanded")

# Page title and description
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        color: #2E86C1;
        text-align: center;
        margin-top: 20px;
    }
    .subheader {
        font-size: 18px;
        color: #34495E;
        text-align: center;
    }
    .footer {
        font-size: 12px;
        color: #7B7D7D;
        text-align: center;
        margin-top: 50px;
    }
    .btn {
        display: block;
        width: 100%;
        margin: 10px 0;
        padding: 10px;
        background-color: #2E86C1;
        color: white;
        font-size: 16px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Gemini AI: Image & Text Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Upload an image, provide optional text, and let the AI analyze and generate a response!</div>', unsafe_allow_html=True)

# Sidebar for input options
st.sidebar.markdown("<h3>Input Options</h3>", unsafe_allow_html=True)

# Text input for the optional description
input_text = st.sidebar.text_input("Enter text to analyze (Optional):")

# Image uploader
uploaded_image = st.sidebar.file_uploader("Upload an image (jpg, jpeg, png):", type=["jpg", "jpeg", "png"])

# Display uploaded image in the main panel
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
else:
    image = None

# Call to action button
submit = st.sidebar.button("Analyze Image", help="Click to analyze the uploaded image and/or text")

# If the submit button is clicked
if submit:
    if image:
        with st.spinner("Analyzing..."):
            try:
                response = get_gemini_response(input_text, image)
                st.subheader("AI Response:")
                st.success(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please upload an image to get a response.")

# Footer for additional styling
st.markdown('<div class="footer">Powered by Google Generative AI - Gemini Model</div>', unsafe_allow_html=True)
