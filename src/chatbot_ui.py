import streamlit as st
from stl import mesh
import numpy as np
import plotly.figure_factory as ff

# Page Config for a clean, wide layout
st.set_page_config(page_title="3D Chatbot", layout="wide")

# Title/Heading
st.title("Modern 3D Chatbot")

# Set up a simple chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input and "Send" button
user_input = st.text_input("Type a message here...")
if st.button("Send"):
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", f"I heard: {user_input}"))

# Display chat messages
for speaker, msg in st.session_state.messages:
    if speaker == "You":
        st.markdown(f"<div style='text-align: right; color: white; background: #007bff; padding: 8px; border-radius: 8px; margin: 5px 0;'>{speaker}: {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; color: black; background: #e2e2e2; padding: 8px; border-radius: 8px; margin: 5px 0;'>{speaker}: {msg}</div>", unsafe_allow_html=True)

# Subheader for 3D Viewer
st.subheader("3D Model Visualization")

# Load STL model
stl_file_path = "C:\\Dev_Projects\\Text-to-3D\\models\\bridge.stl"
your_mesh = mesh.Mesh.from_file(stl_file_path)

# Convert the mesh to plotly format
x, y, z = your_mesh.vectors.reshape(-1, 3).T
i, j, k = np.arange(len(x)).reshape(-1, 3).T

# Plot using Plotly for visualization
fig = ff.create_trisurf(x=x, y=y, z=z, simplices=np.c_[i, j, k])
st.plotly_chart(fig)
