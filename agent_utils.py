from pathlib import Path


def read_agents_md() -> str:
    """Return the contents of AGENTS.md if it exists at the repository root."""
    repo_root = Path(__file__).resolve().parent
    agents_path = repo_root / "AGENTS.md"
    if agents_path.is_file():
        return agents_path.read_text(encoding="utf-8")
    return ""


if __name__ == "__main__":
    content = read_agents_md()
    if content:
        print(content)
    else:
        print("No AGENTS.md found.")
