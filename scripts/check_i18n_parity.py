import json
import sys
from pathlib import Path


def load_keys(p: Path) -> set[str]:
    if not p.exists():
        return set()
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)

    def walk(d, prefix=""):
        keys = set()
        for k, v in d.items():
            full = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                keys |= walk(v, full)
            else:
                keys.add(full)
        return keys

    return walk(data)


en = load_keys(Path("i18n/en.json"))
pl = load_keys(Path("i18n/pl.json"))

missing_in_pl = en - pl
missing_in_en = pl - en

if missing_in_pl or missing_in_en:
    print("i18n parity check FAILED.")
    if missing_in_pl:
        print("Missing in pl.json:", sorted(missing_in_pl))
    if missing_in_en:
        print("Missing in en.json:", sorted(missing_in_en))
    sys.exit(1)
else:
    print("i18n parity check OK.")
