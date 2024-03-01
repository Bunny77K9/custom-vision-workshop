# Part 3: Create and Deploy Streamlit App

## 1. Create the Streamlit App

First, create a new file named `app.py` and paste the Streamlit app code into it.

```python
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
```

## 2. Test the App Locally

Before deploying the app, it's a good idea to test it locally to ensure everything works as expected. You can run the app using the following command in your terminal:

```bash
streamlit run app.py
```

## 3. Deploy to Streamlit Cloud

To deploy the app to Streamlit Cloud, follow these steps:

- Sign in to Streamlit Cloud or create a new account if you haven't already.
- Once logged in, navigate to the dashboard and click on the "New app" button.
- Choose the option to deploy from GitHub and connect your GitHub repository where the app code is located.
- Select the branch containing your app code and specify the path to the app file (e.g., `app.py`).
- After selecting your GitHub repository and branch, you'll reach the "Advanced Settings" section during the deployment process. In this section, you can configure additional settings for your app.
- Look for an option or section labeled "Secrets" or similar. Streamlit Community Cloud allows you to add key-value pairs for environment variables here.
- Add the environment variables required for your app, such as KEY, ENDPOINT, PROJECT_ID, and PUBLISHED_ITERATION_NAME. Enter the appropriate values for each variable.
- Once you've added all the necessary environment variables, save your changes and proceed with the deployment process. Streamlit Community Cloud will now deploy your app with the specified environment variables.
That's it! Your Streamlit app is now deployed and accessible to anyone with the URL. You can continue to make updates to your GitHub repository, and Streamlit Cloud will automatically deploy the changes.


## Summary

Congratulations! You have successfully created and deployed a custom vision app. The app you created can be used to classify dog breeds. You can also create models to detect certain objects in an image. If you want to continue to grow your skills:

- [Object detection with Custom Vision](https://docs.microsoft.com/learn/modules/detect-objects-images-custom-vision/?WT.mc_id=academic-49102-chrhar)
- [Creating custom models with TensorFlow](https://docs.microsoft.com/learn/paths/tensorflow-fundamentals/?WT.mc_id=academic-49102-chrhar)
