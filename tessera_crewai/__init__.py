# ruff: noqa: RUF002
# (U+00D7 MULTIPLICATION SIGN in docstrings is intentional branding glyph, not letter x.)
"""Tessera × CrewAI integration — drop-in cost optimization for any
CrewAI agent / crew.

Usage (most common)::

    from crewai import Agent
    from tessera_crewai import tessera_openai_llm

    llm = tessera_openai_llm(
        model="gpt-4o",
        openai_api_key="sk-...",
        tessera_api_key="tk_...",
    )
    agent = Agent(role="Researcher", goal="...", llm=llm)

    # Existing CrewAI code runs unchanged — agent.execute_task,
    # crew.kickoff, tool calls all route through Tessera proxy.

See https://tesseraai.io/dev for the dashboard, free tier, and full
mechanic documentation.
"""

from tessera_crewai._config import (
    TESSERA_BASE_URL,
    tessera_anthropic_config,
    tessera_anthropic_llm,
    tessera_config,
    tessera_openai_config,
    tessera_openai_llm,
)
from tessera_crewai._version import __version__

__all__ = [
    'TESSERA_BASE_URL',
    '__version__',
    'tessera_anthropic_config',
    'tessera_anthropic_llm',
    'tessera_config',
    'tessera_openai_config',
    'tessera_openai_llm',
]
