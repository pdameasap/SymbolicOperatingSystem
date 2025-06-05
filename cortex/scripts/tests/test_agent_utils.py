from agent_utils import read_agents_md


def test_read_agents_md_present():
    """read_agents_md should return the contents when AGENTS.md exists."""
    content = read_agents_md()
    assert isinstance(content, str)
    assert content.strip() != ""
