import json, yaml
from pathlib import Path
from helper import helper
from datetime import datetime
from app_logs.activity import logger
from fastapi import FastAPI, HTTPException, Form, Request
from module.repo_scanner import clone_git_repo, scan_repo_structure
from model_config.model_config import (
    load_training_examples,
    query_ollama
)

# Paths
LOG_FILE = Path("logs/training_log.jsonl")
TRAINING_FILE = Path("training_data/training_data.yaml")

# Ensure folders exist
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
TRAINING_FILE.parent.mkdir(parents=True, exist_ok=True)

# Ensure empty files exist
if not LOG_FILE.exists():
    LOG_FILE.touch()

if not TRAINING_FILE.exists():
    with open(TRAINING_FILE, "w") as f:
        yaml.dump([], f)


app = FastAPI(
    title="DevOps AI Agent API - Repo Screener",
    description="Analyze Git repo and generate deployment strategy using a local Ollama model.",
    version="1.0"
)


@app.get("/")
def root():
    logger.info("Root endpoint '/' was called.")
    return {"message": "Welcome to the DevOps AI Agent powered by Ollama"}


@app.post("/analyze")
async def analyze_repo(
    request: Request,
    repo_url: str = Form(...),
    instruction: str = Form("Analyze this repo and provide a deployment plan."),
    username: str = Form(None),
    password: str = Form(None)
):
    client_ip = request.client.host
    logger.info(f"analyze request from {client_ip} | Repo: {repo_url}")
    logger.info(f"Instruction: {instruction}")

    try:
        local_repo_path = clone_git_repo(repo_url, username=username, password=password)
        logger.info("Repository cloned successfully.")
    except Exception as e:
        logger.error(f"Failed to clone repository: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to clone repo: {e}")

    repo_files = scan_repo_structure(local_repo_path)
    logger.info(f"Files found in repo: {len(repo_files)}")

    examples = load_training_examples()
    stack = helper.detect_stack(repo_files)
    logger.info(f"Detected tech stack: {stack}")

    prompt = helper.build_prompt(repo_files, examples, stack, instruction)
    logger.debug(f"Prompt sent to Ollama:\n{prompt}")

    result = query_ollama(prompt)
    logger.debug(f"Ollama response:\n{result}")

    log_entry = {
        "timestamp": str(datetime.now()),
        "stack": stack,
        "instruction": instruction,
        "input": "\n".join(repo_files),
        "output": result
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    logger.info("Logged model response to training_log.jsonl")

    with open(TRAINING_FILE, "r") as f:
        try:
            existing = yaml.safe_load(f) or []
        except yaml.YAMLError as ye:
            logger.error(f"YAML read error: {ye}")
            existing = []

    existing_keys = set((item["instruction"], item["input"]) for item in existing)
    new_key = (log_entry["instruction"], log_entry["input"])

    if new_key not in existing_keys:
        existing.append({
            "instruction": log_entry["instruction"],
            "input": log_entry["input"],
            "output": log_entry["output"]
        })
        with open(TRAINING_FILE, "w") as f:
            yaml.dump(existing, f, sort_keys=False)
        logger.info("New training data appended to training_data.yaml")

    return {
        "repo_url": repo_url,
        "repo_files": repo_files,
        "instruction_used": instruction,
        "stack_detected": stack,
        "deployment_plan": result
    }


@app.post("/feedback")
async def submit_feedback(
    request: Request,
    repo_url: str = Form(...),
    corrected_output: str = Form(...),
    instruction: str = Form("Analyze this repo and provide a deployment plan."),
    username: str = Form(default=None),
    password: str = Form(default=None)
):
    client_ip = request.client.host
    logger.info(f"feedback submitted from {client_ip} | Repo: {repo_url}")

    try:
        local_repo_path = clone_git_repo(repo_url, username=username, password=password)
        logger.info("Repo cloned for feedback submission.")
    except Exception as e:
        logger.error(f"Failed to clone repo for feedback: {e}")
        raise HTTPException(status_code=400, detail=f"Repo clone failed: {e}")

    repo_files = scan_repo_structure(local_repo_path)
    logger.info(f"Files found in repo during feedback: {len(repo_files)}")

    stack = helper.detect_stack(repo_files)
    logger.info(f"Detected tech stack during feedback: {stack}")

    log_entry = {
        "timestamp": str(datetime.now()),
        "stack": stack,
        "instruction": instruction,
        "input": "\n".join(repo_files),
        "output": corrected_output
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    logger.info("Feedback logged to training_log.jsonl")

    with open(TRAINING_FILE, "r") as f:
        try:
            existing = yaml.safe_load(f) or []
        except yaml.YAMLError as ye:
            logger.error(f"YAML read error during feedback: {ye}")
            existing = []

    existing_keys = set((item["instruction"], item["input"]) for item in existing)
    new_key = (log_entry["instruction"], log_entry["input"])

    if new_key not in existing_keys:
        existing.append({
            "instruction": log_entry["instruction"],
            "input": log_entry["input"],
            "output": log_entry["output"]
        })
        with open(TRAINING_FILE, "w") as f:
            yaml.dump(existing, f, sort_keys=False)
        logger.info("Feedback appended to training_data.yaml")

    return {
        "message": "Feedback accepted and training data updated",
        "repo_url": repo_url,
        "instruction_used": instruction,
        "stack_detected": stack
    }