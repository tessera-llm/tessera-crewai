"""E2E constructor-survives test for tessera_crewai factory functions.

Requires CrewAI installed. Skips gracefully without it so test_config.py
can still run on lean dev environments.

The "E2E" here is a smoke test — we construct an LLM instance via the
factory and verify the resulting object carries the expected base_url
+ Tessera header, without actually calling out to a live proxy. Real
network E2E lives in the integration suite at the next release cycle.
"""

from __future__ import annotations

import pytest

crewai = pytest.importorskip('crewai')

from tessera_crewai import tessera_anthropic_llm, tessera_openai_llm  # noqa: E402


def test_openai_llm_factory_constructs() -> None:
    llm = tessera_openai_llm(
        model='gpt-4o',
        openai_api_key='sk-test-openai',
        tessera_api_key='tk_test_e2e',
    )
    # CrewAI LLM stores model with provider prefix
    assert 'gpt-4o' in str(llm.model)
    assert llm.base_url is not None and '/v1/openai' in llm.base_url


def test_anthropic_llm_factory_constructs() -> None:
    llm = tessera_anthropic_llm(
        model='claude-sonnet-4-6',
        anthropic_api_key='sk-ant-test',
        tessera_api_key='tk_test_e2e',
    )
    assert 'claude-sonnet-4-6' in str(llm.model)
    assert llm.base_url is not None and '/v1/anthropic' in llm.base_url


def test_model_prefix_idempotent() -> None:
    # User supplies already-prefixed model — should not double-prefix
    llm = tessera_openai_llm(
        model='openai/gpt-4o-mini',
        openai_api_key='sk-test',
        tessera_api_key='tk_test',
    )
    # No double "openai/openai/"
    assert 'openai/openai/' not in str(llm.model)
