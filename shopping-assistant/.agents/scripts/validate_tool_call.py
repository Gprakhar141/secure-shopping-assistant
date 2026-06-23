import json
import re
import sys


def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            # Nothing to validate
            sys.exit(0)

        payload = json.loads(input_data)

        # Check if it's a run_command tool call
        if payload.get("toolName") == "run_command" or "CommandLine" in payload.get(
            "arguments", {}
        ):
            arguments = payload.get("arguments", {})
            command_line = arguments.get("CommandLine", "")

            # Basic check for destructive commands
            destructive_patterns = [
                r"rm\s+-r.*f\s+/",  # Linux/Mac root deletion
                r"rm\s+-r.*f\s+/\*",  # Linux/Mac root deletion
                r"del\s+/s.*[C-Z]:\\",  # Windows recursive deletion
                r"format\s+[a-zA-Z]:",  # Windows disk format
                r"mkfs",  # Linux make filesystem
            ]

            for pattern in destructive_patterns:
                if re.search(pattern, command_line, re.IGNORECASE):
                    print(
                        f"SECURITY BLOCK: The command '{command_line}' matches a destructive pattern and has been blocked.",
                        file=sys.stderr,
                    )
                    sys.exit(1)

    except Exception as e:
        print(f"Validation Hook Error: {e}", file=sys.stderr)
        # Fail closed for security
        sys.exit(1)

    # Allow execution
    sys.exit(0)


if __name__ == "__main__":
    main()
