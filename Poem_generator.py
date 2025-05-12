

from transformers import pipeline, set_seed
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import zipfile

# Load the GPT-2 model
generator = pipeline('text-generation', model='gpt2')
set_seed(42)

# Streamlit Interface
st.title("🎨 Poem Generator using Generative AI")
st.write("Enter a theme, keyword, or first line to generate a poem.")

prompt = st.text_input("Enter your prompt:")

if prompt:
    st.subheader("📝 Generated Poem:")
    output = generator(prompt, max_length=100, num_return_sequences=1)
    poem = output[0]['generated_text']
    st.write(poem)

    # Save poem as image
    def save_poem_image(prompt, poem, filename):
        width, height = 800, 1000
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        wrapped_prompt = textwrap.fill(f"Prompt: {prompt}", width=90)
        wrapped_poem = textwrap.fill(poem, width=90)
        draw.text((20, 20), wrapped_prompt + "\n\n" + wrapped_poem, fill="black", font=font)
        image.save(filename)

    img_filename = "generated_poem.png"
    save_poem_image(prompt, poem, img_filename)
    st.image(img_filename, caption="Poem as Image", use_column_width=True)

    # Create zip for download
    with zipfile.ZipFile("poem_outputs.zip", "w") as zipf:
        zipf.write(img_filename)

    with open("poem_outputs.zip", "rb") as f:
        st.download_button("Download Poem as ZIP", f, file_name="poem_outputs.zip")
