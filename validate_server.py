#!/usr/bin/env python3
"""Validate server.json against the MCP registry schema."""

import json
import sys
from urllib.request import urlopen
from jsonschema import validate, ValidationError, Draft7Validator

SCHEMA_URL = "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json"
SERVER_JSON_PATH = "server.json"

def main():
    print("Fetching schema from:", SCHEMA_URL)
    try:
        with urlopen(SCHEMA_URL) as response:
            schema = json.loads(response.read())
        print("[OK] Schema loaded successfully")
    except Exception as e:
        print(f"[ERROR] Error fetching schema: {e}")
        sys.exit(1)

    print(f"\nLoading server.json from: {SERVER_JSON_PATH}")
    try:
        with open(SERVER_JSON_PATH, 'r', encoding='utf-8') as f:
            server_config = json.load(f)
        print("[OK] server.json loaded successfully")
    except Exception as e:
        print(f"[ERROR] Error loading server.json: {e}")
        sys.exit(1)

    print("\nValidating server.json against schema...")
    try:
        # Create a validator to get more detailed error messages
        validator = Draft7Validator(schema)
        errors = list(validator.iter_errors(server_config))

        if errors:
            print(f"[ERROR] Validation failed with {len(errors)} error(s):\n")
            for i, error in enumerate(errors, 1):
                print(f"{i}. {error.message}")
                print(f"   Path: {' -> '.join(str(p) for p in error.path)}")
                print(f"   Schema path: {' -> '.join(str(p) for p in error.schema_path)}\n")
            sys.exit(1)
        else:
            print("[OK] Validation successful!")
            print("\nserver.json is valid and ready for publishing.")

            # Print summary
            print("\n" + "="*60)
            print("Server Configuration Summary:")
            print("="*60)
            print(f"Name: {server_config.get('name')}")
            print(f"Title: {server_config.get('title')}")
            print(f"Version: {server_config.get('version')}")
            print(f"Description: {server_config.get('description')}")
            if 'remotes' in server_config:
                print(f"\nRemote Endpoints:")
                for remote in server_config['remotes']:
                    print(f"  - Type: {remote.get('type')}")
                    print(f"    URL: {remote.get('url')}")
            print("="*60)

    except ValidationError as e:
        print(f"[ERROR] Validation error: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error during validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
