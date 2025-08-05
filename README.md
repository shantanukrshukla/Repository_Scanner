# DevOps AI Agent - Repo Screener

## Overview

**DevOps AI Agent - Repo Screener** is an intelligent FastAPI-based service that analyzes Git repositories and generates secure, cloud-native deployment strategies using a local Ollama LLM model. It supports feedback-driven learning, enabling continuous improvement of deployment recommendations.

---

## Features

- **Git Repo Analysis:** Clones and scans public or private Git repositories.
- **Tech Stack Detection:** Automatically identifies the main technology stack (Node.js, Python, Go, etc.).
- **Deployment Plan Generation:** Uses a local Ollama model to suggest secure, cloud-native deployment strategies.
- **Feedback Loop:** Accepts user feedback to improve future recommendations.
- **Training Data Logging:** Stores all interactions and feedback for further model fine-tuning.
- **REST API:** Exposes endpoints for analysis and feedback submission.

---

## Project Structure

```
main.py
test_main.http
app_logs/
    activity.py
helper/
    helper.py
model_config/
    model_config.py
module/
    repo_scanner.py
logs/
    training_log.jsonl
training_data/
    training_data.yaml
training_docs/
    training_data.yml
```

---

## How It Works

1. **Clone & Scan:** The API clones the provided Git repository and scans its file structure.
2. **Stack Detection:** Determines the main technology stack using heuristics in [`helper/helper.py`](helper/helper.py).
3. **Prompt Construction:** Builds a prompt for the Ollama LLM using real examples and the detected stack.
4. **LLM Query:** Sends the prompt to the local Ollama model to generate a deployment plan.
5. **Logging & Feedback:** Logs the request/response and allows users to submit corrections, which are added to the training data.

---

## API Endpoints

### `GET /`
- Health check and welcome message.

### `POST /analyze`
- **Parameters:**  
  - `repo_url` (str, required): Git repository URL  
  - `instruction` (str, optional): Custom instruction for the LLM  
  - `username` (str, optional): Git username (for private repos)  
  - `password` (str, optional): Git password/token (for private repos)
- **Response:**  
  - Detected stack, repo files, deployment plan, etc.

### `POST /feedback`
- **Parameters:**  
  - `repo_url` (str, required): Git repository URL  
  - `corrected_output` (str, required): Improved/corrected deployment plan  
  - `instruction` (str, optional): Instruction used  
  - `username` (str, optional): Git username  
  - `password` (str, optional): Git password/token
- **Response:**  
  - Confirmation message and updated training data

---

## Example Usage

### Analyze a Repository

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -F "repo_url=https://github.com/your/repo.git"
```

### Submit Feedback

```bash
curl -X POST http://127.0.0.1:8000/feedback \
  -F "repo_url=https://github.com/your/repo.git" \
  -F "corrected_output=Your improved deployment plan here"
```

---

## Training Data & Logging

- **Training Data:**  
  - [`training_data/training_data.yaml`](training_data/training_data.yaml) — Stores unique instruction/input/output triples for model improvement.
  - [`training_docs/training_data.yml`](training_docs/training_data.yml) — Example training data for prompt construction.
- **Logs:**  
  - [`logs/training_log.jsonl`](logs/training_log.jsonl) — All analysis and feedback requests are logged here.

---

## Development & Extensibility

- **Stack Detection:**  
  - Easily extendable in [`helper/helper.py`](helper/helper.py) to support more stacks.
- **Prompt Engineering:**  
  - Prompt templates and example selection logic in [`helper/helper.py`](helper/helper.py) and [`model_config/model_config.py`](model_config/model_config.py).
- **Model Integration:**  
  - Uses Ollama's local LLM via the [Ollama Python SDK](https://ollama.com/).

---

## Requirements

- Python 3.8+
- FastAPI
- PyYAML
- GitPython
- Ollama Python SDK

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the API

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

You can now access the API at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## License

MIT License

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Ollama](https://ollama.com/)
- [GitPython](https://gitpython.readthedocs.io/)