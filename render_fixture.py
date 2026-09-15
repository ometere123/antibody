"""Render entrypoint for the API-only synthetic Antibody fixture."""

from __future__ import annotations

import os
from http.server import HTTPServer

from fixtures.test_agent import Handler


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    print(f"Antibody synthetic fixture listening on 0.0.0.0:{port}", flush=True)
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
