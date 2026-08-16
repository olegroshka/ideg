"""Securely save and verify the IBM Quantum account used by AR-023.

The API key is read from an environment variable when available, otherwise
with hidden terminal input.  It is never accepted as a command-line argument,
printed, returned, or written outside Qiskit Runtime's credential store.
"""

from __future__ import annotations

import argparse
from getpass import getpass
import os
from pathlib import Path


DEFAULT_CREDENTIAL_FILE = (
    Path(os.environ.get("USERPROFILE", str(Path.home())))
    / "Documents" / "Codex" / ".credentials" / "ideg-qiskit-ibm.json"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instance", default="open-instance",
                        help="IBM Quantum instance name or CRN")
    parser.add_argument("--name", default="ideg-open",
                        help="local Qiskit credential profile name")
    parser.add_argument("--overwrite", action="store_true",
                        help="replace an existing profile with this name")
    parser.add_argument("--credentials-file", type=Path,
                        default=DEFAULT_CREDENTIAL_FILE,
                        help="private Qiskit account file outside the repo")
    parser.add_argument("--token-env", default="IBM_QUANTUM",
                        help="environment variable containing the API key")
    args = parser.parse_args()

    from qiskit_ibm_runtime import QiskitRuntimeService

    credential_file = args.credentials_file.expanduser().resolve()
    credential_file.parent.mkdir(parents=True, exist_ok=True)
    print(f"Credential file: {credential_file}")
    token = os.environ.get(args.token_env, "").strip()
    if token:
        print(f"Using API key from environment variable: {args.token_env}")
    else:
        print("Paste the API key at the next prompt and press Enter. "
              "No characters will appear while you type.")
        token = getpass("IBM Quantum API key (hidden): ").strip()
    if not token:
        raise ValueError("API key cannot be empty")
    try:
        QiskitRuntimeService.save_account(
            channel="ibm_quantum_platform",
            token=token,
            instance=args.instance,
            name=args.name,
            filename=str(credential_file),
            overwrite=args.overwrite,
            set_as_default=False,
        )
    finally:
        token = ""

    service = QiskitRuntimeService(name=args.name,
                                   filename=str(credential_file))
    backends = service.backends(operational=True, simulator=False)
    print(f"Saved profile: {args.name}")
    print(f"Active instance: {service.active_instance()}")
    print("Operational QPUs: " + ", ".join(sorted(
        backend.name for backend in backends
    )))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
