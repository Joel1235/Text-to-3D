import requests
import os
import trimesh
import time
import datetime
import logging

from dotenv import load_dotenv; load_dotenv()

api_key = os.getenv("MESHY_API_KEY")
meshy_url = os.getenv("MESHY_URL")

#orders meshy generation for user input
def generate_3d_meshy(user_input: str):
    payload = {
      "mode": "preview",
      "prompt": user_input,
      "art_style": "realistic",
      "should_remesh": True
    }

    headers = { "Authorization": f"Bearer {api_key}" }
    response = requests.post(meshy_url, headers=headers, json=payload)

    data = response.json()
    try:
        result_id = data["result"]
        logging.info("Meshy generation successful: Result ID %s", result_id)
        return result_id, "Success"
    except KeyError:
        logging.error("Meshy generation failed: %s", data.get("error", "Unknown error"))
        return None, "Meshy generation failed, try again later"


#Download and save meshy model
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
    logging.info("Model downloaded: %s", full_path)
    print("Your model was generated and is saved at: " + full_path)
    return full_path


#Check regularly if meshy generation is finished
def wait_fo_meshy_generation(result_id: str, max_attempts=60, interval = 5):
    headers = {"Authorization": f"Bearer {api_key}"}
    for _ in range(max_attempts):
        response = requests.get(f"{meshy_url}/{result_id}", headers=headers)
        response.raise_for_status()
        task_status = response.json()

        if task_status["status"] == "SUCCEEDED":
            logging.info("3D model generation completed successfully.")
            return True
        print(f"Status: {task_status['status']} | Progress: {task_status.get('progress', 'N/A')} | Retrying in {interval}s...")
        time.sleep(interval)
    logging.error("Timeout reached while waiting for 3D model generation.")
    return False
