import requests
import os
import trimesh
import time
import datetime

from dotenv import load_dotenv; load_dotenv()

api_key = os.getenv("MESHY_API_KEY")
meshy_url = os.getenv("MESHY_URL")

def generate_3d_meshy(user_input: str):
    payload = {
      "mode": "preview",
      "prompt": user_input,
      "art_style": "realistic",
      "should_remesh": True
    }

    headers = { "Authorization": f"Bearer {api_key}" }
    response = requests.post(meshy_url, headers=headers, json=payload)
    #response.raise_for_status()  #TODO: maybe return a second string which indicates if the creation was successfully commissioned

    data = response.json()
    result_id = data["result"]
    return result_id

def download_meshy_model(result_id: str):
    model_url = f"{meshy_url}/{result_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(model_url, headers=headers)

    data = response.json()
    glb_url = data["model_urls"]["glb"]
    response = requests.get(glb_url)

    filename = datetime.datetime.now().strftime("model_%Y%m%d_%H%M%S.glb")
    path = r"C:\Dev_Projects\Text-to-3D\generated_models"
    full_path = f"{path}\\{filename}"
    with open(full_path, "wb") as file:
        file.write(response.content)
    print(f"Model saved as {filename} in {path}")
    # mesh = trimesh.load(filename)
    # mesh.show()
    return full_path

#generation_id = generate_3d_meshy("A helicopter")
#downlaod_meshy_model(generation_id)





#generate_3d_meshy()


"""result_text = "{'result': '019479b0-c088-75ae-b831-f19b4900bb3a'} # This is what meshy gives you back"
result_id = "019479b0-c088-75ae-b831-f19b4900bb3a"
url = f"https://api.meshy.ai/openapi/v2/text-to-3d/{result_id}"
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(url, headers=headers)
print(response.json())

data = response.json()
glb_url = data["model_urls"]["glb"]
response = requests.get(glb_url)

with open("model.glb", "wb") as file:
    file.write(response.content)
print("Model downloaded successfully!")

mesh = trimesh.load("model.glb")
mesh.show()"""

