import streamlit as st
import trimesh
import os
import pandas as pd
import numpy as np
import time
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from services.llm_service import llm_req
from services.meshy_service import generate_3d_meshy, download_meshy_model, wait_fo_meshy_generation
import plotly.figure_factory as ff

# Page Config for a clean, wide layout
st.set_page_config(page_title="3D Chatbot", layout="wide")

# Title/Heading
st.title("3D Model Assistant")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')
objects_path = os.path.join(os.getcwd(), "models", "objects.csv")
object_list = pd.read_csv(objects_path)["Filename"].tolist()


def get_validation_prompt(user_input):
    return f"""
    Determine if the following input is a reasonable request for generating a 3D object. 
    Valid requests should describe a tangible or conceptual object that can be visualized in 3D, even if creatively described. 
    If the input is appropriate, respond with "true". If it is irrelevant, respond with "false".
    Input: {user_input}
    """


def get_matching_prompt(user_input, best_match):
    return f"""
    Based on the user's request: "{user_input}", determine if the 3D model: "{best_match}" is a suitable match. 
    Respond only with "true" if it meets expectations, otherwise respond with "false".
    """


def get_generation_prompt(user_input):
    return f"""
    Analyze the user's request: "{user_input}" and extract the precise object.
    Respond with only the extracted object.
    """


def validate_input(user_input):
    validation_prompt = get_validation_prompt(user_input)
    return llm_req(validation_prompt, "").lower() == "true"


def find_best_match(user_input):
    class_embeddings = model.encode(object_list)
    input_embedding = model.encode([user_input])
    similarities = cosine_similarity(input_embedding, class_embeddings)
    return object_list[similarities.argmax()]


def assess_model_match(user_input, best_match):
    prompt = get_matching_prompt(user_input, best_match)
    return llm_req(prompt, "").lower() == "false"


def generate_3d_model(user_input):
    prompt = get_generation_prompt(user_input)
    return llm_req(prompt, "")


user_input = st.text_input("Type a message here...")
if st.button("Send"):
    if user_input:
        st.session_state.messages.append(("You", user_input))

        if validate_input(user_input):
            st.session_state.messages.append(("Bot", "Processing your request..."))
            best_match = find_best_match(user_input)

            if assess_model_match(user_input, best_match):
                generation_object = generate_3d_model(user_input)
                meshy_generation_id = generate_3d_meshy(generation_object)
                st.session_state.messages.append(("Bot", "Generating 3D model, please wait..."))

                if wait_fo_meshy_generation(meshy_generation_id):
                    model_filename = download_meshy_model(meshy_generation_id)
            else:
                model_filename = os.path.join(os.getcwd(), "models", f"{best_match}.stl")

            if model_filename:
                mesh = trimesh.load(model_filename)
                if isinstance(mesh, trimesh.Scene):
                    mesh = mesh.dump(concatenate=True)
                vertices, faces = mesh.vertices, mesh.faces
                x, y, z = vertices.T
                i, j, k = faces.T
                fig = ff.create_trisurf(x=x, y=y, z=z, simplices=np.c_[i, j, k])
                st.plotly_chart(fig)
                st.session_state.messages.append(("Bot", "Here is your 3D model."))
        else:
            st.session_state.messages.append(("Bot", "Invalid request. Please try again."))

for speaker, msg in st.session_state.messages:
    if speaker == "You":
        st.markdown(
            f"<div style='text-align: right; color: white; background: #007bff; padding: 8px; border-radius: 8px; margin: 5px 0;'>{speaker}: {msg}</div>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='text-align: left; color: black; background: #e2e2e2; padding: 8px; border-radius: 8px; margin: 5px 0;'>{speaker}: {msg}</div>",
            unsafe_allow_html=True)
