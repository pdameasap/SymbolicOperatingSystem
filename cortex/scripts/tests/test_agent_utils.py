from agent_utils import read_agents_md


def test_read_agents_md_absent():
    """read_agents_md should return an empty string when AGENTS.md is missing."""
    content = read_agents_md()
    assert content == ""
