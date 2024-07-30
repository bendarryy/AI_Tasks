import base64
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from io import BytesIO
from PIL import Image

st.title("Chat with images")
st.subheader("Gemini + LangChain")


def convert_to_base64(image_file_path):
    """
    Convert PIL images to Base64 encoded strings

    :param pil_image: PIL image
    :return: Re-sized Base64 string
    """

    pil_image = Image.open(image_file_path)

    buffered = BytesIO()
    pil_image.save(buffered, format="png")  # You can change the format if needed
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def upload_image():
    image = st.file_uploader("Upload an image to chat about", type=["png", "jpg", "jpeg"])
    if image:
        images_b64 = [1]

        # display images in multiple columns
        cols = st.columns(len(images_b64))
        for i, col in enumerate(cols):
            col.markdown(f"*Image {i+1}*")
            col.image(image)
        st.markdown("---")
        #return images_b64

        return convert_to_base64(image)
    st.stop()


@st.cache_data(show_spinner=False)
def ask_vllm(question, image_b64):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",google_api_key="AIzaSyBj43wl7kUvuKVEAwoO_WFuLiapz0M8WPc")
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": question,
            },  # You can optionally provide text parts
            {
                "type": "image_url", 
                "image_url": f"data:image/jpeg;base64,{image_b64}" 
            },
        ]
    )
    res = llm.invoke([message])
    return res


def app():
    c1, c2 = st.columns(2)
    with c2:
        image_b64 = upload_image()
    with c1:
        question = st.chat_input("Ask a question about the image(s)")
    if not question: st.stop()
    with c1:
        with st.chat_message("question"):
            st.markdown(question, unsafe_allow_html=True)
        with st.spinner("Thinking..."):
            res = ask_vllm(question, image_b64)
            with st.chat_message("response"):
                st.write(res.content)


if __name__== "__main__":
    app()