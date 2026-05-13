#!/usr/bin/env python3
"""
Download GOV.UK Frontend assets into static/govuk-frontend/.
TODO: Run in pipeline builds: python scripts/setup_govuk_frontend.py
"""

import io
import sys
import zipfile
from pathlib import Path

VERSION = "6.1.0"

DEST = Path(__file__).resolve().parent.parent / "static" / "govuk-frontend"
URL = f"https://github.com/alphagov/govuk-frontend/releases/download/v{VERSION}/release-v{VERSION}.zip"

ASSETS = [
    f"govuk-frontend-{VERSION}.min.css",
    f"govuk-frontend-{VERSION}.min.js",
    f"govuk-frontend-{VERSION}.min.css.map",
    f"govuk-frontend-{VERSION}.min.js.map",
]

GENERIC_NAMES = {
    f"govuk-frontend-{VERSION}.min.css": "govuk-frontend.min.css",
    f"govuk-frontend-{VERSION}.min.js": "govuk-frontend.min.js",
    f"govuk-frontend-{VERSION}.min.css.map": "govuk-frontend.min.css.map",
    f"govuk-frontend-{VERSION}.min.js.map": "govuk-frontend.min.js.map",
}

IMAGE_ASSETS = [
    "favicon.ico",
    "favicon.svg",
    "govuk-icon-mask.svg",
    "govuk-icon-512.png",
    "govuk-icon-192.png",
    "govuk-icon-180.png",
    "govuk-crest.svg",
    "govuk-opengraph-image.png",
]


def fix_govuk_jinja_symlinks():
    """
    govuk-frontend-jinja uses internal imports like
    govuk_frontend_jinja/macros/attributes.html but the actual files
    live at govuk_frontend_jinja/templates/macros/attributes.html.
    Symlinks fix this without modifying the package.
    """
    import govuk_frontend_jinja

    package_dir = Path(govuk_frontend_jinja.__file__).parent

    for folder in ["macros", "components"]:
        link = package_dir / folder
        target = package_dir / "templates" / folder
        if not link.exists():
            link.symlink_to(target)
            print(f"  created symlink: {link} -> {target}")
        else:
            print(f"  symlink already exists: {link}")


def main():
    try:
        import requests
    except ImportError:
        try:
            import urllib.request as req

            requests = None
        except ImportError:
            print("Install requests: pip install requests")
            sys.exit(1)

    DEST.mkdir(parents=True, exist_ok=True)
    images_dir = DEST.parent / "images"
    images_dir.mkdir(exist_ok=True)

    if all((DEST / f).exists() for f in ASSETS):
        print(f"GOV.UK Frontend v{VERSION} already present — skipping.")
        return

    print(f"Downloading GOV.UK Frontend v{VERSION}…")

    if requests:
        data = requests.get(URL, timeout=60).content
    else:
        with req.urlopen(URL) as r:
            data = r.read()

    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for name in zf.namelist():
            filename = Path(name).name
            if filename in ASSETS:
                (DEST / filename).write_bytes(zf.read(name))
                print(f"  {filename}")
            if filename in IMAGE_ASSETS:
                (images_dir / filename).write_bytes(zf.read(name))
                print(f"  images/{filename}")

    print("Done.")
    print("Fixing jinja symlinks")
    fix_govuk_jinja_symlinks()


if __name__ == "__main__":
    main()
