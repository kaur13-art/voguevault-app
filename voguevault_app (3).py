import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO

# Secure OpenAI client initialization
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="VogueVault", layout="wide")
st.title("👗 VogueVault - Your AI Fashion Stylist")

# Sidebar: User inputs
st.sidebar.header("Personal Info")
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
height = st.sidebar.selectbox("Height", ["4ft-5ft", "5.1ft-5.5ft", "5.6ft-6ft", "6.1ft-6.5ft"])
complexion = st.sidebar.selectbox("Complexion", ["Fair", "Wheatish", "Dark"])
style = st.sidebar.selectbox("Fashion Style", ["Old Money", "New Money", "Party", "Wedding"])
wedding_culture = None
if style == "Wedding":
    wedding_culture = st.sidebar.selectbox("Wedding Culture", ["Sikh", "Hindu", "Muslim", "Christian"])
uploaded_file = st.sidebar.file_uploader("Upload Full Body Image (Optional)", type=["jpg", "jpeg", "png"])

def generate_prompt():
    gender_term = gender.lower()
    height_term = "petite" if "4" in height else "average height" if "5.5" in height else "tall"
    complexion_term = complexion.lower()
    prompt = f"A photorealistic full-body fashion outfit for a {complexion_term}-skinned {height_term} {gender_term} person. "
    styles = {
        "Old Money": "Classic, sophisticated outfit with high-quality fabrics and timeless cuts.",
        "New Money": "Trendy, bold fashion with luxury and designer elements.",
        "Party": "Fun, vibrant evening or celebration wear.",
        "Wedding": f"Formal {wedding_culture} wedding outfit with traditional and modern blend."
    }
    prompt += styles[style]
    prompt += " High quality fashion magazine photography."
    return prompt

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

if st.button("✨ Generate Outfit Recommendations"):
    with st.spinner("Generating with AI..."):
        base_prompt = generate_prompt()
        variations = [
            base_prompt + " Front view.",
            base_prompt + " Three-quarter view.",
            base_prompt + " Different color scheme."
        ]
        images = []
        for p in variations:
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=p,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                img_url = response.data[0].url
                img_data = requests.get(img_url).content
                images.append(Image.open(BytesIO(img_data)))
            except Exception as e:
                st.error(f"Image generation failed: {e}")

        st.subheader("🖼️ Recommended Outfits")
        cols = st.columns(3)
        for i, img in enumerate(images):
            with cols[i % 3]:
                st.image(img, caption=f"Look {i+1}", use_column_width=True)
                with st.expander("💬 Buy This Look"):
                    st.markdown(f"[📩 Message us on WhatsApp](https://wa.me/your_number_here?text=I'm+interested+in+Look+{i+1}+from+VogueVault)")
