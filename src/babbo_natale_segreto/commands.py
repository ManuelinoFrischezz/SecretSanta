import subprocess
import sys


def run_sorteggio():

    script_path = "src/babbo_natale_segreto/extraction.py"

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        return (
            True,
            "✅ Draw completed successfully!",
        )

    return (
        False,
        result.stderr,
    )
