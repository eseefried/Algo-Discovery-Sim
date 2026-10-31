.PHONY: setup test lint vaults smoke bench report

setup:
	uv sync --group dev

test:
	uv run pytest -q

lint:
	uv run ruff check src tests

vaults:
	uv run a2m check-vault arxiv-1407.6402
	uv run a2m check-vault arxiv-1411.5949

# Offline end-to-end check of the harness (scripted mock LLM, no key needed).
smoke:
	uv run a2m bench --llm mock --seeds 1 --systems swarm,single_agent,central_planner --quiet

# Real benchmark. Spends money: every system gets configs/default.yaml budget per run.
bench:
	uv run a2m bench --seeds 3 --systems swarm,single_agent,single_agent_small,central_planner

report:
	uv run a2m report
