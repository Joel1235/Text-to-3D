# 3D Model Generation with RAG + Meshy

Welcome to our 3D model generation project, conducted as a coursework of the Data-Driven Engineering lecture in WS 2024/25 in the University of Paderborn. 
We leverage **Retrieval-Augmented Generation (RAG)** and **Meshy AI** to try to generate high-quality 3D models from textual descriptions.

## 🚀 Live Demo

Check out the fastest way to test our app via the live demo, which we deployed with Streamlit.

🔗 **[Live Demo on Streamlit](https://joeldag.streamlit.app/)**

All in all the live demo should be robust with some restrictions: 
Please be aware that the meshy generation does not work if multiple users use it simultaneously.
The life demo might not be perfect and might contain bugs, e.g. clicking multiple times on the send button might bring the meshy generation to failure.

## 🛠 Installation Guide

If you'd prefer to run the project locally, follow these steps:

1. **Clone the repository:** (or use the zip file)
   ```bash
   git clone https://git.uni-paderborn.de/deilers/ddeai.git
   cd ddeai
   ```

2. **Pull Git LFS files:**
   Ensure Git LFS is installed, then pull the large files tracked with LFS.

   ```bash
   git lfs install
   git lfs pull
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create the `.env` file**  
   In the project's root directory, create a `.env` file with the required environment variables:

   ```env
    API_KEY =
    LLM_URL =
    MESHY_API_KEY =
    MESHY_URL =
   ```
   The .env file including all the api keys and links will be included in the .zip of the submission. 

6. **Run the Streamlit UI:**
   ```bash
   streamlit run src/chatbot_ui.py
   ```

## 🖥 Alternative Terminal-Based Usage

If the new UI contains bugs or you prefer a command-line approach, you can still generate 3D models using our classic terminal-based script:

1. **Run the script**:
```bash
python src/main.py
```
2. **Enter your Request**: The script asks you to enter a request a CAD model. For instance use
```
"Give me a CAD model of a sportscar" 
```
3. **Model generation**: The script uses RAG of MeshyAPI to generate the model.
The model is saved in the models folder. The script will reutrn you the exact locate you 3D model is saved to.

## ⚠ Known Issues

- The new UI is under active development and may contain minor bugs.
- If you encounter issues, feel free to fall back to the terminal-based script.

---

