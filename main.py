import io
import streamlit as st
from huggingface_hub import InferenceClient
import config

st.set_page_config(page_title="AI Avatar Creator", page_icon="🎨", layout="centered")


OPTIONS = {

"avatar type": ["boy hero", "girl hero", "wizard", "robot explorer", "space warrior", "animal adventurer"],

"hairstyle": ["short spiky hair", "curly hair", "long straight hair", "ponytail", "glowing hair", "helmet"],

"outfit": ["superhero suit", "magical robe", "space armor", "casual hoodie", "battle costume", "royal outfit"],

"expression": ["happy", "confident", "excited", "brave", "mysterious", "playful"],

"background": ["forest", "space station", "magic castle", "city skyline", "rainbow world", "cloud kingdom"],

"art style": ["cartoon style", "anime style", "3D game style", "fantasy illustration", "comic style"],

}

client = InferenceClient(api_key=config.HF_API_KEY)
st.session_state.setdefault("generated_image", None)

st.title("🎨 AI Avatar Creator")
st.write("Create your own unique avatar by selecting different attributes!")
st.markdown("Choose your avatar details or write your own custom prompt for a personalized avatar. Then click the generate button.")
st.subheader("Create Your Avatar")

mode = st.selectbox ('Choose Prompt Mode' , ['Use Avatar Builder', 'Write Custom Prompt'])

if mode == 'Use Avatar Builder':
    values = {k: st.selectbox(f'Choose {k}:', v) for k, v in OPTIONS.items()}
    extra = st.text_input("Or add extra details (optional):", placeholder="e.g., glowing eyes, futuristic background")

prompt = (

f"A kid friendly {values['avatar type']} "

f"with {values['hairstyle']} "

f"wearing a {values['outfit']} "

f"with a {values['expression']} expression "

f"set against a {values['background']} colorful, digital highly detailed background "

f"in a {values['art style']} art style. {extra}"

)
final_prompt = f"{prompt} {extra}" if extra else prompt
else:
    final_prompt = st.text_area("Enter your custom prompt:", placeholder="e.g., A futuristic robot with neon lights in a cyberpunk cityscape, digital art style", height =150).strip()
    
    with st.expander("See Final Prompt"):
        st.write(final_prompt or "your final prompt will appear here once you generate the image")

if st.button("Generate Avatar"):

        if not config.HF_API_KEY:
            st.error("Please set your Hugging Face API key in the .env file.")
        elif not final_prompt:
            st.error("Please enter a prompt to generate an avatar.")
        else:
            with st.spinner("Generating your avatar..."):
                try:
                    st.session_state.generated_image = client.text_to_image(
                    prompt=final_prompt,
                    model=config.HF_IMAGE_MODEL
                    )
                    st.success("Avatar generated successfully!")
                except Exception as e:
                    st.error(f"Error generating avatar: {e}")

    if st.session_state.generated_image:
        st.image(st.session_state.generated_image, caption="Your AI Avatar", use_container_width=True)
        buffer = io.BytesIO()
        st.session_state.generated_image.save(buffer, format="PNG")
        st.download_button(
            "Download Avatar",
            data=buffer.getvalue(),
            file_name="ai_avatar.png",
            mime="image/png"
        )




