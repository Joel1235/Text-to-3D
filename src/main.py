import pandas as pd
import os
import trimesh
import time
import datetime

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from services.llm_service import llm_req
from prompts.prompts import PROMPT_VALIDATION
from services.meshy_service import generate_3d_meshy
from services.meshy_service import download_meshy_model
from services.meshy_service import wait_fo_meshy_generation

model = SentenceTransformer('all-MiniLM-L6-v2')
validation_sys_prompt = "You are an AI assistant responsible for validating user inputs for 3D model generation. Your goal is to allow creative and descriptive requests while filtering out irrelevant or nonsensical inputs."

validation_prompt = f"""
Determine if the following input is a reasonable request for generating a 3D object. 
Valid requests should describe a tangible or conceptual object that can be visualized in 3D, even if creatively described. 
If the input is appropriate, respond with "true". If it is irrelevant, nonsensical, or unrelated to 3D objects, respond with "false". No additional text or explanations.
Input: """


objects_path = os.path.join(os.getcwd(), "models", "objects.csv")
object_list = pd.read_csv(objects_path)["Filename"].tolist()
print(object_list)
#user_input = "Give me a 3D model of a Truck"
user_input = input("Enter your request: ")
validation_response = llm_req(validation_prompt + user_input, validation_sys_prompt)
input_valid: bool = validation_response.lower() == "true"

if input_valid:
    print("Input was valid, continue process")
    # embed and get best object class
    class_embeddings = model.encode(object_list)
    input_embedding = model.encode([user_input])
    similarities = cosine_similarity(input_embedding, class_embeddings)
    best_match = object_list[similarities.argmax()]
    print(f"best object in data: {best_match}")

    system_prompt_1 = "You are an expert in 3D model retrieval and user satisfaction analysis. Your task is to assess whether a proposed 3D model aligns with user expectations."
    prompt_1 = f"""
    Based on the user's request: "{user_input}", determine if the 3D model: "{best_match}" is a suitable match. 
    Respond only with "true" if it meets expectations, otherwise respond with "false". No additional text.
    """
    new_creation_response = llm_req(prompt_1, system_prompt_1)
    new_creation: bool = new_creation_response.lower() == "false"  #meaning if it will not satisfy the user, set this value (new_creation) to true

    if new_creation:
        system_prompt_2 = "You are an AI assistant specializing in accurately extracting object descriptions for 3D model generation, ensuring all key attributes and details from user input are preserved."
        prompt_2 = f"""
        Analyze the user's request: "{user_input}" and extract the precise object along with its essential attributes to generate an accurate 3D model. 
        For example, if the request includes specific characteristics or modifications, include them in the response. 
        Respond with only the extracted object description without any additional text or explanations.
        """
        generation_object = llm_req(prompt_2, system_prompt_2)
        print("Object which will get generated: " + generation_object)
        meshy_generation_id = generate_3d_meshy(generation_object)
        if(wait_fo_meshy_generation(meshy_generation_id)):
            model_filename = download_meshy_model(meshy_generation_id)
            mesh = trimesh.load(model_filename)
            mesh.show()
    else:
        model_path = os.path.join(os.getcwd(), "models")
        cad_model_path = os.path.join(model_path, f"{best_match}.stl")
        if cad_model_path:
            print(f"Open Cad mdoel file: {cad_model_path}")
            mesh = trimesh.load(cad_model_path)
            mesh.show()
else:
    print("Input was invalid, ask for a 3D model")