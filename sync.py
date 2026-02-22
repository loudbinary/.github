#!/usr/bin/env python3
"""Sync new product items into the products registry for user selection.

This script is a LOCAL action for this repository.
Product consumers should call their own product-start.py, not this script directly.
"""
import json
import os

PRODUCTS_FILE = "products.json"


def load_registry():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE) as f:
            return json.load(f)
    return {"products": []}


def sync(items):
    """Merge new product items into the registry, skipping duplicates."""
    registry = load_registry()
    existing = {p["name"] for p in registry["products"]}
    added = []
    for item in items:
        if item["name"] not in existing:
            registry["products"].append(item)
            added.append(item["name"])
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(registry, f, indent=2)
    return added


if __name__ == "__main__":
    new_items = [
        {"name": "starter", "description": "Loudbinary Starter Package"},
        {"name": "pro", "description": "Loudbinary Pro Package"},
    ]
    added = sync(new_items)
    if added:
        print(f"Synced {len(added)} product(s): {', '.join(added)}")
    else:
        print("Products already up to date, nothing to sync")
    print("Sync complete")
