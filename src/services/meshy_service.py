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
    path = os.path.join(os.getcwd(), "models")
    full_path = f"{path}\\{filename}"
    with open(full_path, "wb") as file:
        file.write(response.content)
    print(f"Model saved as {filename} in {path}")
    # mesh = trimesh.load(filename)
    # mesh.show()
    return full_path

def wait_fo_meshy_generation(result_id: str, max_attempts=30, interval = 5):
    headers = {"Authorization": f"Bearer {api_key}"}
    for _ in range(max_attempts):
        response = requests.get(f"{meshy_url}/{result_id}", headers=headers)
        response.raise_for_status()
        task_status = response.json()

        if task_status["status"] == "SUCCEEDED":
            print("3D model meshy generation completed ")
            return True
        print(f"Status: {task_status['status']} | Progress: {task_status.get('progress', 'N/A')} | Retrying in {interval}s...")
        time.sleep(interval)
    print("Time out waiting for 3D model meshy generation")
    return False
