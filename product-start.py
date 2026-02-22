#!/usr/bin/env python3
"""Bootstrap GitHub Actions for a product in the loudbinary org.

Run this once inside a product repository to:
  - Generate the minimal workflow that hooks into org-level reusable workflows
  - Give the org control points (e.g. sync, policy checks) without extra work per team

Usage:
    python product-start.py --product-name <name> [--description <desc>]

What it does NOT do:
    - Call sync.py directly (that is the org's responsibility via loudbinary-start.yaml)
"""
import argparse
import json
import os


WORKFLOW_TEMPLATE = """\
name: {product_name} CI

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  # Org-provided control point: runs org-level checks and sync without extra work.
  org-control:
    uses: loudbinary/.github/.github/workflows/loudbinary-start.yaml@main
    secrets: inherit
"""


REGISTRATION_FILE = os.path.join(".github", "product-registration.json")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Bootstrap GitHub Actions for a loudbinary org product"
    )
    parser.add_argument("--product-name", required=True, help="Product name (slug)")
    parser.add_argument("--description", default="", help="Short product description")
    return parser.parse_args()


def write_workflow(product_name):
    """Write the minimal CI workflow file into the product repo."""
    workflows_dir = os.path.join(".github", "workflows")
    os.makedirs(workflows_dir, exist_ok=True)
    workflow_path = os.path.join(workflows_dir, "ci.yaml")
    content = WORKFLOW_TEMPLATE.format(product_name=product_name)
    with open(workflow_path, "w") as f:
        f.write(content)
    print(f"Created workflow: {workflow_path}")
    return workflow_path


def register_product(product_name, description):
    """Write a product-registration.json into .github/ for the org sync to discover.

    sync.py (in loudbinary/.github) reads these files when it scans org repositories,
    merging each registered product into the central products.json registry.
    """
    record = {"name": product_name, "description": description}
    os.makedirs(".github", exist_ok=True)
    with open(REGISTRATION_FILE, "w") as f:
        json.dump(record, f, indent=2)
    print(f"Wrote product registration: {REGISTRATION_FILE}")
    return record


def main():
    args = parse_args()
    write_workflow(args.product_name)
    register_product(args.product_name, args.description)
    print("Product start complete")


if __name__ == "__main__":
    main()
