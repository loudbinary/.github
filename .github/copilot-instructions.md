# Copilot Instructions

This is the `loudbinary/.github` repository — the organisation-level `.github` repo for the **loudbinary** GitHub organisation. Changes here affect all repositories in the org that rely on shared workflows and the product registry.

## Repository layout

```
.github/
  products/            # Per-product start configurations (<product>-start.yaml)
  workflows/           # Shared GitHub Actions workflows
    catch-all.yml      # Primary workflow: validates sync.py, dispatches products
    loudbinary-start.yaml  # Reusable workflow: sets up Python and runs sync.py
    run-tests.yaml     # CI: runs tests/test_act.sh against the workflow
products.json          # Central product registry (source of truth)
sync.py                # Merges new products into products.json (run at org level)
product-start.py       # Bootstrap script run inside individual product repos
scripts/sync.py        # Lightweight stub invoked by synced-repo workflows
tests/test_act.sh      # Integration test using `act` to exercise loudbinary-start.yaml
```

## Key conventions

- **Python**: All Python files use `#!/usr/bin/env python3` and include a module-level docstring. Keep scripts self-contained (no third-party dependencies beyond the standard library).
- **`products.json`**: The registry holds `{"products": [{"name": ..., "description": ...}, ...]}`. `sync.py` is the only writer; it skips duplicates by name.
- **Workflows**: Use `actions/checkout@v4` and `actions/setup-python@v5` (Python `'3.x'`). Reusable workflows live in `.github/workflows/` and are called with `uses: loudbinary/.github/.github/workflows/<file>@main`.
- **Product files**: Each product has a corresponding `.github/products/<product>-start.yaml`. The `catch-all.yml` workflow checks for this file to decide whether to execute or onboard a product.
- **`scripts/sync.py`**: This is a lightweight stub (`sys.exit(0)`) used as the *first action* in synced product-repo workflows. It intentionally contains no business logic — do not add any here. All real sync logic lives in the root-level `sync.py`.

## How to test

- Run `python sync.py` from the repo root to verify the sync script exits cleanly (exit 0).
- Run `bash tests/test_act.sh` (requires [`act`](https://github.com/nektos/act)) to execute `loudbinary-start.yaml` locally and confirm `sync.py` prints `Sync complete`.
- CI runs both checks automatically via `.github/workflows/run-tests.yaml` and the `test-sync` job in `catch-all.yml`.

## Adding a new product

1. Run `python product-start.py --product-name <name> --description "<desc>"` inside the product repo. This generates `.github/workflows/ci.yaml` and `.github/product-registration.json`.
2. In this repo, add the product slug to the `options` list in `catch-all.yml` under `workflow_dispatch.inputs.product`.
3. Create `.github/products/<name>-start.yaml` following the pattern in `loudbinary-start.yaml`.
4. Trigger the `Catch-All` workflow with the new product selected, or let the `onboard-product` job scaffold the files automatically if the product file is missing.

## Important notes

- Do not commit secrets or credentials. Secrets are managed via GitHub Environments.
- The `loudbinary` GitHub Environment must exist in this repository with `PRODUCT=loudbinary` set before the `execute-product` job can run.
- Keep `products.json` and `sync.py` in sync: every product slug that `sync.py` lists in `new_items` should eventually appear in `products.json`.
