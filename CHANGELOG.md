# Changelog — tessera-crewai

All notable changes to this package are documented here. Versioning follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). Wire format
compatibility across minor versions (0.X.Y) — breaking changes only on
major bumps.

## [0.1.0] — 2026-05-19 — first scaffold (monorepo)

- 2 verified provider config functions (`tessera_openai_config`,
  `tessera_anthropic_config`) returning the kwargs spread accepted by
  CrewAI's `LLM(...)` constructor: `base_url` + `extra_headers`.
- 2 lazy-import factory functions (`tessera_openai_llm`,
  `tessera_anthropic_llm`) constructing a pre-wired `crewai.LLM`
  instance — handles model-id prefix idempotency (`openai/` /
  `anthropic/`) so callers can pass either bare or prefixed strings.
- Generic dispatcher `tessera_config(provider, api_key, ...)` for
  callers iterating across providers.
- Unit-test coverage for config-dict shape + dispatcher error paths.
  E2E constructor-survives tests gate on CrewAI availability via
  `pytest.importorskip` so they degrade gracefully on lean envs.
- py.typed marker — full type hints exposed to downstream type checkers.

Publication to PyPI deferred until the next release cycle. Package
lives in the Tessera monorepo under `packages/tessera-crewai/` for the
scaffold cycle.
