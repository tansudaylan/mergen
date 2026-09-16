"""Mergen tutorial example.

This file is intentionally import-safe and only runs when executed directly.
"""

import mergen


def main():
    """Create a lightweight instance and return it without running a heavy workflow on import."""
    objtmerg = mergen.mergen()
    objtmerg.folder_initiate()
    return objtmerg


if __name__ == '__main__':
    main()

