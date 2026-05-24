"""Provider config + factory functions for routing CrewAI agents through
the Tessera proxy.

CrewAI's `LLM` class wraps LiteLLM under the hood and accepts `base_url`,
`api_key`, and `extra_headers` keyword arguments. Tessera's proxy speaks
the OpenAI + Anthropic wire formats at `/v1/<provider>` paths, so the
integration is a thin shim: point CrewAI's LLM at the proxy endpoint
with the customer's provider API key and pass the Tessera key in
`x-tessera-api-key` header.

Field names verified against CrewAI v0.80+ source (2026-05-19):
- LLM(model, api_key, base_url, extra_headers, ...) — LiteLLM-shape
- model strings are prefixed with provider: "openai/gpt-4o", "anthropic/claude-sonnet-4-6"

OpenAI + Anthropic are the v0.1 verified providers, covering ~85% of
customer traffic per outreach research. Mistral / Groq / Cohere
Providers exist in CrewAI but their custom-header passthrough has not
been verified end-to-end at v0.1 time — queued for v0.2.
"""

from __future__ import annotations

from typing import Any, Literal

TESSERA_BASE_URL = 'https://api.tesseraai.io'

ProviderName = Literal['openai', 'anthropic']


def _validate_api_key(api_key: str) -> str:
    if not isinstance(api_key, str) or not api_key:
        raise ValueError(
            'tessera_*_config(api_key=...) requires a non-empty string. '
            'Get a free key from https://tesseraai.io/dev'
        )
    return api_key


def _proxy_endpoint(provider: ProviderName) -> str:
    return f'{TESSERA_BASE_URL}/v1/{provider}'


def _headers(api_key: str, extra: dict[str, str] | None = None) -> dict[str, str]:
    headers = {'x-tessera-api-key': api_key}
    if extra:
        headers.update(extra)
    return headers


def tessera_openai_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `crewai.LLM(...)` to route OpenAI-shape requests through Tessera.

    Example::

        from crewai import LLM, Agent
        from tessera_crewai import tessera_openai_config

        llm = LLM(
            model="openai/gpt-4o",
            api_key="sk-...",  # your OpenAI key
            **tessera_openai_config(api_key="tk_..."),
        )
        agent = Agent(role="Researcher", goal="...", llm=llm)
    """
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('openai')
    return {
        'base_url': endpoint,
        'extra_headers': _headers(api_key, extra_headers),
    }


def tessera_anthropic_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `crewai.LLM(...)` to route Anthropic-shape requests through Tessera.

    Example::

        from crewai import LLM, Agent
        from tessera_crewai import tessera_anthropic_config

        llm = LLM(
            model="anthropic/claude-sonnet-4-6",
            api_key="sk-ant-...",  # your Anthropic key
            **tessera_anthropic_config(api_key="tk_..."),
        )
        agent = Agent(role="Researcher", goal="...", llm=llm)
    """
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('anthropic')
    return {
        'base_url': endpoint,
        'extra_headers': _headers(api_key, extra_headers),
    }


def tessera_config(
    provider: ProviderName,
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Generic dispatcher — returns the right kwargs dict for the given provider."""
    mapping = {
        'openai': tessera_openai_config,
        'anthropic': tessera_anthropic_config,
    }
    if provider not in mapping:
        raise ValueError(
            f'Unknown provider {provider!r}. Supported: {list(mapping)}. '
            'Mistral / Groq / Cohere are queued for v0.2 — see the README.'
        )
    return mapping[provider](api_key=api_key, extra_headers=extra_headers, base_url=base_url)


def tessera_openai_llm(
    model: str,
    openai_api_key: str,
    tessera_api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
    **llm_kwargs: Any,
) -> Any:
    """Construct a CrewAI `LLM` pre-wired to Tessera's OpenAI-shape proxy.

    Imports `crewai.LLM` lazily so this module imports cleanly without
    CrewAI installed.

    `model` should be the bare OpenAI model id (e.g. "gpt-4o") — the
    helper prefixes "openai/" automatically for LiteLLM's provider
    routing convention.

    Example::

        from crewai import Agent
        from tessera_crewai import tessera_openai_llm

        llm = tessera_openai_llm(
            model="gpt-4o",
            openai_api_key="sk-...",
            tessera_api_key="tk_...",
        )
        agent = Agent(role="Researcher", goal="...", llm=llm)
    """
    from crewai import LLM  # type: ignore[import-not-found]

    cfg = tessera_openai_config(
        api_key=tessera_api_key, extra_headers=extra_headers, base_url=base_url
    )
    return LLM(
        model=model if '/' in model else f'openai/{model}',
        api_key=openai_api_key,
        **cfg,
        **llm_kwargs,
    )


def tessera_anthropic_llm(
    model: str,
    anthropic_api_key: str,
    tessera_api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
    **llm_kwargs: Any,
) -> Any:
    """Construct a CrewAI `LLM` pre-wired to Tessera's Anthropic-shape proxy.

    Imports `crewai.LLM` lazily. `model` should be the bare Anthropic
    model id (e.g. "claude-sonnet-4-6") — helper prefixes "anthropic/".

    Example::

        from crewai import Agent
        from tessera_crewai import tessera_anthropic_llm

        llm = tessera_anthropic_llm(
            model="claude-sonnet-4-6",
            anthropic_api_key="sk-ant-...",
            tessera_api_key="tk_...",
        )
        agent = Agent(role="Researcher", goal="...", llm=llm)
    """
    from crewai import LLM  # type: ignore[import-not-found]

    cfg = tessera_anthropic_config(
        api_key=tessera_api_key, extra_headers=extra_headers, base_url=base_url
    )
    return LLM(
        model=model if '/' in model else f'anthropic/{model}',
        api_key=anthropic_api_key,
        **cfg,
        **llm_kwargs,
    )
