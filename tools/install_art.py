#!/usr/bin/env python3
"""Install full-body portraits and matching transparent dragon tokens.

Input layout:
  artwork/portraits/<dragon-key>.png|jpg|jpeg|webp
  artwork/tokens/<dragon-key>.png|webp     (optional if --remove-bg is used)

Run:
  python -m pip install pillow
  python tools/install_art.py --input artwork --dry-run
  python tools/install_art.py --input artwork --remove-bg
  (cd tools && npm install && node pack.mjs)

For --remove-bg, also install "rembg[cpu]" and its model dependencies.
All 36 dragon types are required for a complete batch. The installer fails
before writing files if any required source or alpha processing is missing.
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Install Pillow first: python -m pip install pillow") from exc

ROOT = Path(__file__).resolve().parent.parent
AGES = ("wyrmling", "young", "adult", "ancient")
SOURCE = ROOT / "src" / "legacy-dragons"
MODULE = "legacy-dragons"
EXTS = (".png", ".webp", ".jpg", ".jpeg")


def source_image(directory: Path, key: str) -> Path | None:
    matches = [directory / (key + ext) for ext in EXTS if (directory / (key + ext)).is_file()]
    if len(matches) > 1:
        raise ValueError(f"Multiple images for {key} in {directory}: {matches}")
    return matches[0] if matches else None


def open_rgba(path: Path) -> Image.Image:
    with Image.open(path) as image:
        image.load()
        return image.convert("RGBA")


def remove_background(image: Image.Image) -> Image.Image:
    try:
        from rembg import remove
    except ImportError as exc:
        raise RuntimeError("Background removal requested. Install rembg[cpu] first.") from exc
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    result = remove(bio.getvalue())
    return Image.open(io.BytesIO(result)).convert("RGBA")


def make_portrait(image: Image.Image) -> Image.Image:
    # Preserve composition and transparency, and avoid upscaling small sources.
    image.thumbnail((1600, 2400), Image.Resampling.LANCZOS)
    return image


def make_token(image: Image.Image) -> Image.Image:
    alpha = image.getchannel("A")
    min_alpha, max_alpha = alpha.getextrema()
    if min_alpha >= 245 or max_alpha <= 8:
        raise ValueError("Token requires real transparency; provide transparent token art or --remove-bg")
    bbox = alpha.point(lambda value: 255 if value >= 24 else 0).getbbox()
    if bbox is None:
        raise ValueError("Token foreground mask is empty")
    x0, y0, x1, y1 = bbox
    w, h = x1 - x0, y1 - y0
    margin = max(5, int(max(w, h) * 0.06))
    x0, y0 = max(0, x0 - margin), max(0, y0 - margin)
    x1, y1 = min(image.width, x1 + margin), min(image.height, y1 + margin)
    crop = image.crop((x0, y0, x1, y1))
    crop.thumbnail((720, 720), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (768, 768), (0, 0, 0, 0))
    canvas.alpha_composite(crop, ((768 - crop.width) // 2, (768 - crop.height) // 2))
    if canvas.getpixel((0, 0))[3] != 0:
        raise ValueError("Token corners must be transparent")
    return canvas


def save_webp(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="WEBP", quality=90, method=6, exact=True)


def actor_paths(key: str) -> tuple[str, str]:
    return (
        f"modules/{MODULE}/portraits/{key}.webp",
        f"modules/{MODULE}/tokens/{key}.webp",
    )


def updated_actor(text: str, key: str) -> str:
    actor = json.loads(text)
    portrait, token = actor_paths(key)
    if actor.get("flags", {}).get(MODULE, {}).get("dragon") != key:
        raise ValueError(f"Source actor does not belong to {key}")
    actor["img"] = portrait
    actor["prototypeToken"]["texture"]["src"] = token
    # Keep existing actor ID, item IDs, stats, and all gameplay fields intact.
    return json.dumps(actor, indent=1, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Directory containing portraits/ and optional tokens/")
    parser.add_argument("--remove-bg", action="store_true", help="Use rembg to derive transparent tokens from portraits")
    parser.add_argument("--dry-run", action="store_true", help="Verify inputs without writing")
    parser.add_argument("--pack", action="store_true", help="Compile the Foundry compendium after installation")
    args = parser.parse_args()

    specs = json.loads((ROOT / "tools" / "artwork_prompts.json").read_text())
    items = {entry["key"]: entry for entry in specs}
    if len(items) != 36:
        raise SystemExit(f"Expected 36 distinct dragon types, got {len(items)}")

    portraits_dir = args.input / "portraits"
    tokens_dir = args.input / "tokens"
    sources = {}
    missing = []
    for key in items:
        portrait = source_image(portraits_dir, key)
        token = source_image(tokens_dir, key)
        if not portrait:
            missing.append(f"{key}: portrait")
        if not token and not args.remove_bg:
            missing.append(f"{key}: transparent token (or use --remove-bg)")
        for age in AGES:
            if not (SOURCE / f"{key}-{age}.json").is_file():
                missing.append(f"{key}: missing source actor {age}")
        sources[key] = portrait, token
    if missing:
        raise SystemExit("Missing required inputs:\n  " + "\n  ".join(missing))
    print(f"Validated sources for {len(items)} dragon types and {len(items)*4} actors.")
    if args.dry_run:
        return

    # Stage every file first; don't overwrite existing artwork on partial failures.
    with tempfile.TemporaryDirectory(prefix="legacy-dragons-art-") as tmp:
        stage = Path(tmp)
        for key, (portrait_src, token_src) in sources.items():
            full = open_rgba(portrait_src)
            portrait = make_portrait(full.copy())
            cutout = open_rgba(token_src) if token_src else remove_background(full)
            token = make_token(cutout)
            save_webp(portrait, stage / "portraits" / f"{key}.webp")
            save_webp(token, stage / "tokens" / f"{key}.webp")
            for age in AGES:
                name = f"{key}-{age}.json"
                source_text = (SOURCE / name).read_text()
                revised = updated_actor(source_text, key)
                (stage / name).write_text(revised)
            print(f"  {key}: portrait + transparent token + four actor references")

        # All conversion and validation succeeded. Only now update source tree.
        for key in items:
            for folder in ("portraits", "tokens"):
                target = ROOT / folder / f"{key}.webp"
                target.parent.mkdir(parents=True, exist_ok=True)
                (stage / folder / f"{key}.webp").replace(target)
            for age in AGES:
                name = f"{key}-{age}.json"
                (stage / name).replace(SOURCE / name)

    if args.pack:
        cli = ROOT / "tools" / "node_modules"
        if not cli.is_dir():
            raise SystemExit("Images installed, but compendium was not rebuilt. Run: (cd tools && npm install && node pack.mjs)")
        subprocess.run(["node", "tools/pack.mjs"], cwd=ROOT, check=True)
    else:
        print("Now rebuild the compendium with: (cd tools && npm install && node pack.mjs)")
    print("Artwork installed: 36 portraits, 36 transparent tokens, 144 linked actor sources.")


if __name__ == "__main__":
    main()
