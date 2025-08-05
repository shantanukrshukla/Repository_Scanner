import yaml
import ollama

def load_training_examples(file_path="/Users/shantanukumarshukla/PycharmProjects/Repo_Scanner/training_docs/training_data.yml"):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def generate_prompt(repo_structure: list, examples: list):
    prompt = "You are a DevOps expert. Analyze the repo structure and suggest a deployment strategy.\n\n"
    for ex in examples:
        prompt += f"### Instruction:\n{ex['instruction']}\n"
        prompt += f"### Files:\n{ex['input']}\n"
        prompt += f"### Plan:\n{ex['output']}\n\n"

    prompt += "### Instruction:\nAnalyze this repo:\n"
    prompt += "### Files:\n" + "\n".join(repo_structure) + "\n"
    prompt += "### Plan:\n"
    return prompt

def query_ollama(prompt: str, model='llama3:8b'):
    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']
