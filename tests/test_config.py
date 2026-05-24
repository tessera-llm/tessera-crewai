"""Unit tests for tessera_crewai._config — pure-function shape verification.

E2E LLM-construction tests live in test_e2e.py and require CrewAI installed
(skipped when import fails). This file tests the config dicts only, so it
runs without the crewai dependency.
"""

from __future__ import annotations

import pytest

from tessera_crewai import (
    TESSERA_BASE_URL,
    tessera_anthropic_config,
    tessera_config,
    tessera_openai_config,
)


class TestTesseraOpenAIConfig:
    def test_base_url_points_at_openai_proxy(self) -> None:
        cfg = tessera_openai_config(api_key='tk_test')
        assert cfg['base_url'] == f'{TESSERA_BASE_URL}/v1/openai'

    def test_headers_carry_tessera_key(self) -> None:
        cfg = tessera_openai_config(api_key='tk_test_key_abc')
        assert cfg['extra_headers']['x-tessera-api-key'] == 'tk_test_key_abc'

    def test_extra_headers_merge(self) -> None:
        cfg = tessera_openai_config(
            api_key='tk_test',
            extra_headers={'x-custom': 'value'},
        )
        assert cfg['extra_headers']['x-tessera-api-key'] == 'tk_test'
        assert cfg['extra_headers']['x-custom'] == 'value'

    def test_base_url_override(self) -> None:
        cfg = tessera_openai_config(
            api_key='tk_test',
            base_url='https://staging.tesseraai.io/v1/openai',
        )
        assert cfg['base_url'] == 'https://staging.tesseraai.io/v1/openai'

    def test_empty_api_key_raises(self) -> None:
        with pytest.raises(ValueError):
            tessera_openai_config(api_key='')

    def test_non_string_api_key_raises(self) -> None:
        with pytest.raises(ValueError):
            tessera_openai_config(api_key=None)  # type: ignore[arg-type]


class TestTesseraAnthropicConfig:
    def test_base_url_points_at_anthropic_proxy(self) -> None:
        cfg = tessera_anthropic_config(api_key='tk_test')
        assert cfg['base_url'] == f'{TESSERA_BASE_URL}/v1/anthropic'

    def test_headers_carry_tessera_key(self) -> None:
        cfg = tessera_anthropic_config(api_key='tk_test_anth')
        assert cfg['extra_headers']['x-tessera-api-key'] == 'tk_test_anth'


class TestTesseraConfigDispatcher:
    def test_dispatches_to_openai(self) -> None:
        cfg = tessera_config('openai', api_key='tk_test')
        assert '/v1/openai' in cfg['base_url']

    def test_dispatches_to_anthropic(self) -> None:
        cfg = tessera_config('anthropic', api_key='tk_test')
        assert '/v1/anthropic' in cfg['base_url']

    def test_unknown_provider_raises(self) -> None:
        with pytest.raises(ValueError, match='Unknown provider'):
            tessera_config('mistral', api_key='tk_test')  # type: ignore[arg-type]

    def test_forwards_extra_headers(self) -> None:
        cfg = tessera_config(
            'openai',
            api_key='tk_test',
            extra_headers={'x-feature-tag': 'research'},
        )
        assert cfg['extra_headers']['x-feature-tag'] == 'research'
