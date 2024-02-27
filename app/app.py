import streamlit as st
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import requests
from PIL import Image
from io import BytesIO
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Load Azure Custom Vision credentials
KEY = os.getenv('KEY')
ENDPOINT = os.getenv('ENDPOINT')
PROJECT_ID = os.getenv('PROJECT_ID')
PUBLISHED_ITERATION_NAME = os.getenv('PUBLISHED_ITERATION_NAME')

# Create prediction client
credentials = ApiKeyCredentials(in_headers={'Prediction-key': KEY})
client = CustomVisionPredictionClient(ENDPOINT, credentials)

# Function to perform prediction
def predict_image(image):
    results = client.classify_image(PROJECT_ID, PUBLISHED_ITERATION_NAME, image)
    return results.predictions

# Streamlit app
def main():
    st.title("Dog Breed Prediction App")

    # User input: image upload or URL
    option = st.radio("Choose Input Option:", ('Upload Image', 'Image URL'))

    if option == 'Upload Image':
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = uploaded_file.read()
            st.image(image, caption='Uploaded Image', use_column_width=True)
            predictions = predict_image(image)
            display_predictions(predictions)

    elif option == 'Image URL':
        image_url = st.text_input("Enter Image URL:")
        if image_url:
            try:
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                st.image(image, caption='Image URL', use_column_width=True)
                image_bytes = BytesIO()
                image.save(image_bytes, format="JPEG")
                predictions = predict_image(image_bytes.getvalue())
                display_predictions(predictions)
            except Exception as e:
                st.error("Error loading image from URL. Please check the URL and try again.")

# Function to display predictions
def display_predictions(predictions):
    st.subheader("Predictions:")
    if predictions:
        for prediction in predictions:
            st.write(f"{prediction.tag_name}: {prediction.probability:.2%}")
        # Get the breed with highest probability
        top_prediction = predictions[0]
        breed = top_prediction.tag_name
        st.write(f"### Yay! It's a {breed} 🐶", unsafe_allow_html=True)
    else:
        st.write("No predictions available.")

if __name__ == "__main__":
    main()
