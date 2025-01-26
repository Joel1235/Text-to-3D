import pandas as pd
import os
import trimesh
import time
import datetime
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from services.llm_service import llm_req
from services.meshy_service import generate_3d_meshy, download_meshy_model, wait_fo_meshy_generation

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Paths
objects_path = os.path.join(os.getcwd(), "models", "objects.csv")

# Prompts
def get_validation_prompt(user_input):
    return f"""
    Determine if the following input is a reasonable request for generating a 3D object. 
    Valid requests should describe a tangible or conceptual object that can be visualized in 3D, even if creatively described. 
    If the input is appropriate, respond with "true". If it is irrelevant, nonsensical, or unrelated to 3D objects, respond with "false". No additional text or explanations.
    Input: {user_input}
    """

def get_matching_prompt(user_input, best_match):
    return f"""
    Based on the user's request: "{user_input}", determine if the 3D model: "{best_match}" is a suitable match. 
    Respond only with "true" if it meets expectations, otherwise respond with "false". No additional text.
    """

def get_generation_prompt(user_input):
    return f"""
    Analyze the user's request: "{user_input}" and extract the precise object along with its essential attributes to generate an accurate 3D model. 
    Respond with only the extracted object description without any additional text or explanations.
    """

def validate_input(user_input):
    validation_prompt = get_validation_prompt(user_input)
    sys_prompt = "You are an AI assistant responsible for validating user inputs for 3D model generation. Your goal is to allow creative and descriptive requests while filtering out irrelevant or nonsensical inputs."
    return llm_req(validation_prompt, sys_prompt).lower() == "true"

def find_best_match(user_input, object_list):
    class_embeddings = model.encode(object_list)
    input_embedding = model.encode([user_input])
    similarities = cosine_similarity(input_embedding, class_embeddings)
    return object_list[similarities.argmax()]

def assess_model_match(user_input, best_match):
    prompt = get_matching_prompt(user_input, best_match)
    sys_prompt = "You are an expert in 3D model retrieval and user satisfaction analysis. Your task is to assess whether a proposed 3D model aligns with user expectations."
    return llm_req(prompt, sys_prompt).lower() == "false"

def generate_3d_model(user_input):
    prompt = get_generation_prompt(user_input)
    sys_prompt = "You are an AI assistant specializing in accurately extracting object descriptions for 3D model generation, ensuring all key attributes and details from user input are preserved."
    return llm_req(prompt, sys_prompt)

def process_request():
    object_list = pd.read_csv(objects_path)["Filename"].tolist()
    print(object_list)

    user_input = input("Enter your request: ")

    if not validate_input(user_input):
        print("Input was invalid, ask for a 3D model")
        return

    print("Input was valid, continue process")
    best_match = find_best_match(user_input, object_list)
    print(f"Best object in data: {best_match}")

    if assess_model_match(user_input, best_match):
        generation_object = generate_3d_model(user_input)
        print("Object which will get generated: " + generation_object)
        meshy_generation_id = generate_3d_meshy(generation_object)

        if wait_fo_meshy_generation(meshy_generation_id):
            model_filename = download_meshy_model(meshy_generation_id)
            mesh = trimesh.load(model_filename)
            mesh.show()
    else:
        cad_model_path = os.path.join(os.getcwd(), "models", f"{best_match}.stl")
        print(f"Open CAD model file: {cad_model_path}")
        mesh = trimesh.load(cad_model_path)
        mesh.show()

if __name__ == "__main__":
    process_request()
