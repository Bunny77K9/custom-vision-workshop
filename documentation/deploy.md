# Part 3: Create and Deploy Streamlit App

### ✅ Directory Structure

```
dog-breed-app/
├── .env.example          # Sample environment variable file
├── requirements.txt      # Python dependencies
├── app/
│   └── streamlit_app.py  # Streamlit app code
```

---

## ⚙️ Part 2: Prepare the Environment

### ✅ 1. Create a virtual environment

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

---

### ✅ 2. Install dependencies

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should contain:

```txt
streamlit
azure-cognitiveservices-vision-customvision
msrest
python-dotenv
requests
Pillow
```

---

### ✅ 3. Create a `.env` file

Make a copy of `.env.example` and rename it to `.env`, then fill in your Azure Custom Vision credentials:

```bash
cp .env.example .env  # Use `copy .env.example .env` on Windows
```

Edit `.env`:

```env
KEY=your_azure_prediction_key
ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
PROJECT_ID=your_project_id
PUBLISHED_ITERATION_NAME=your_iteration_name
```

---

## 👨‍💻 Part 3: Create and Deploy Streamlit App

### ✅ 1. Create the Streamlit App

In `app/streamlit_app.py`, paste the following code:

```python
import streamlit as st
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import requests
from PIL import Image
from io import BytesIO
import os

from dotenv import load_dotenv
load_dotenv()

KEY = os.getenv('KEY')
ENDPOINT = os.getenv('ENDPOINT')
PROJECT_ID = os.getenv('PROJECT_ID')
PUBLISHED_ITERATION_NAME = os.getenv('PUBLISHED_ITERATION_NAME')

credentials = ApiKeyCredentials(in_headers={'Prediction-key': KEY})
client = CustomVisionPredictionClient(ENDPOINT, credentials)

def predict_image(image):
    results = client.classify_image(PROJECT_ID, PUBLISHED_ITERATION_NAME, image)
    return results.predictions

def main():
    st.title("🐶 Dog Breed Prediction App")

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

def display_predictions(predictions):
    st.subheader("Predictions:")
    if predictions:
        for prediction in predictions:
            st.write(f"{prediction.tag_name}: {prediction.probability:.2%}")
        top_prediction = predictions[0]
        breed = top_prediction.tag_name
        st.write(f"### Yay! It's a {breed} 🐶", unsafe_allow_html=True)
    else:
        st.write("No predictions available.")

if __name__ == "__main__":
    main()
```

---

### ✅ 2. Test the App Locally

Run the app from the **project root**:

```bash
streamlit run app/streamlit_app.py
```

Then open the browser at [http://localhost:8501](http://localhost:8501)

---

## 🚀 Part 4: Deploy to Streamlit Cloud

1. **Push your code** to a GitHub repository (public or private).

2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud) and sign in.

3. Click **"New app"** and choose your GitHub repository.

4. In the **App file path**, set:

   ```
   app/streamlit_app.py
   ```

5. In **Advanced Settings**, set environment variables:

   | Name                       | Value                        |
   | -------------------------- | ---------------------------- |
   | `KEY`                      | your Azure Custom Vision key |
   | `ENDPOINT`                 | your endpoint URL            |
   | `PROJECT_ID`               | your project ID              |
   | `PUBLISHED_ITERATION_NAME` | your iteration name          |

6. Click **Deploy** — your app is live! 🎉

---

## ✅ Summary

You’ve now:

* Built a full-stack image classification app with Streamlit and Azure
* Used environment variables for secure configuration
* Deployed the app to Streamlit Community Cloud

---

## 📚 Continue Learning

* [🔍 Object detection with Custom Vision](https://learn.microsoft.com/en-us/training/modules/detect-objects-images-custom-vision/)
* [🧠 TensorFlow Fundamentals](https://learn.microsoft.com/en-us/training/paths/tensorflow-fundamentals/)

---

Let me know if you want to add **Docker support**, **CI/CD with GitHub Actions**, or a **custom domain** setup.
