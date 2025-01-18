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

model = SentenceTransformer('all-MiniLM-L6-v2')
dataset_path = f"C:\Dev_Projects\Text-to-3D\data\ModelNet40"

classes = [d.name for d in os.scandir(dataset_path) if d.is_dir()]
print(classes)
user_input = "Give me a 3D model of a Truck"
#user_input = input("Enter your request: ")
validation_response = llm_req(PROMPT_VALIDATION + user_input)
input_valid: bool = validation_response.lower() == "true"

if input_valid:
    print("Input was valid, continue process")
    # embed and get best object class
    class_embeddings = model.encode(classes)
    input_embedding = model.encode([user_input])
    similarities = cosine_similarity(input_embedding, class_embeddings)
    best_match = classes[similarities.argmax()]
    print(f"best class in data: {best_match}")

    prompt = f"""
    Evalaute if this object {best_match} will satisfy the users input: {user_input} regarding returning a 3D model.
    If it will likely satisfy the users expectations, answer with "true". If not, respond with "false". Do not output anything else.
    """
    new_creation_response = llm_req(prompt)
    new_creation: bool = new_creation_response.lower() == "false"  #meaning if it will not satisfy the user, set this value (new_creation) to true

    if new_creation:
        prompt= f"""
        From this users input: {user_input} precisely extract the object the user want to generate. 
        E.g If the users request is "Give me a 3D model of a Flower", then only return "A Flower".
        Do not output anything else. 
        """
        generation_object = llm_req(prompt)
        meshy_generation_id = generate_3d_meshy(generation_object)
        print("Generation of 3D model sent to meshy, wait 60 until finished")
        time.sleep(60)
        print("60s watied, check if model is finished")

        #Get model and show
        model_filename = download_meshy_model(meshy_generation_id)
        mesh = trimesh.load(model_filename)
        mesh.show()
    else:
        cad_model_path = rf"C:\Dev_Projects\Text-to-3D\data\ModelNet40\{best_match}\test"
        first_file_path = next((os.path.join(cad_model_path, f) for f in os.listdir(cad_model_path) if f.endswith('.off')), None) #for now we can just take the first valid 3d model in the files with the matching class
        if first_file_path:
            print(f"First .off file path: {first_file_path}")
            mesh = trimesh.load(first_file_path)
            mesh.show()
else:
    print("Input was invalid, ask for a 3D model")