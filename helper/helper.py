def detect_stack(repo_files: list[str]) -> str:
    if any(f.endswith(".py") for f in repo_files):
        return "Python"
    elif any(f.endswith(".go") for f in repo_files):
        return "Go"
    elif any("package.json" in f for f in repo_files):
        return "Node.js"
    elif any("vite.config.js" in f or "index.jsx" in f for f in repo_files):
        return "React.js"
    elif any(f.endswith(".csproj") or f.endswith(".cs") for f in repo_files):
        return ".NET"
    elif any(f.endswith(".java") or "pom.xml" in f for f in repo_files):
        return "Java"
    elif any(f.endswith(".rs") for f in repo_files):
        return "Rust"
    elif any(f.endswith(".php") for f in repo_files):
        return "PHP"
    else:
        return "Unknown"


def build_prompt(repo_files: list[str], examples: list[dict], stack: str, instruction: str) -> str:
    stack_examples = [e for e in examples if stack.lower() in e["output"].lower()]

    if not stack_examples:
        return f"""{instruction}

Stack: {stack}
Repo file structure:
{chr(10).join(repo_files)}

There are no specific examples yet. Please provide a generic, secure, and cloud-native deployment strategy."""
    else:
        prompt = f"{instruction}\nUse the following examples to infer a deployment strategy.\n\n"
        for ex in stack_examples[:3]:  # Top 3 relevant examples
            prompt += f"""### Example
Input:
{ex['input']}

Output:
{ex['output']}

"""
        prompt += f"### New Project\nInput:\n{chr(10).join(repo_files)}\n\nOutput:"
        return prompt

