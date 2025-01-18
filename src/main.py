import pandas as pd
import os
import trimesh

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from services.llm_service import validate_user_input

model = SentenceTransformer('all-MiniLM-L6-v2')
dataset_path = f"C:\Dev_Projects\Text-to-3D\data\ModelNet40"

classes = [d.name for d in os.scandir(dataset_path) if d.is_dir()]
print(classes)
#user_input = "Give me a 3D model of a Flower"
user_input = input("Enter your request: ")
input_valid = validate_user_input(user_input)

if input_valid:
    # embed and get best object class
    class_embeddings = model.encode(classes)
    input_embedding = model.encode([user_input])
    similarities = cosine_similarity(input_embedding, class_embeddings)
    best_match = classes[similarities.argmax()]

    print(f"best class in data: {best_match}")
    cad_model_path = rf"C:\Dev_Projects\Text-to-3D\data\ModelNet40\{best_match}\test"
    first_file_path = next((os.path.join(cad_model_path, f) for f in os.listdir(cad_model_path) if f.endswith('.off')), None) #for now we can just take the first valid 3d model in the files with the matching class
    if first_file_path:
        print(f"First .off file path: {first_file_path}")
        mesh = trimesh.load(first_file_path)
        mesh.show()
    else:
        print("No .off files found.")
