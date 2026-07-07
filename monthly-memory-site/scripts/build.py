# -*- coding: utf-8 -*-
"""
自动扫描 memories/ 文件夹，生成网站需要的内容清单 manifest.json。
你永远不需要手动运行它，GitHub 会在你每次上传文件后自动执行。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEM = ROOT / "memories"

IMG = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VID = {".mp4", ".mov", ".webm", ".m4v"}
AUD = {".mp3", ".m4a", ".wav", ".ogg", ".flac"}

manifest = {}

for ydir in sorted(MEM.iterdir()):
    if not ydir.is_dir() or not ydir.name.isdigit():
        continue
    year = {}
    for mdir in sorted(ydir.iterdir()):
        if not mdir.is_dir():
            continue
        mm = mdir.name
        entry = {"summary": "", "song": "", "artist": "", "audio": "", "cover": "", "items": []}
        for f in sorted(mdir.iterdir(), key=lambda p: p.name.lower()):
            if f.name.lower() == "summary.txt":
                body = []
                for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                    s = line.strip()
                    if s.startswith("歌名:") or s.startswith("歌名："):
                        entry["song"] = s[3:].strip()
                    elif s.startswith("歌手:") or s.startswith("歌手："):
                        entry["artist"] = s[3:].strip()
                    else:
                        body.append(line)
                entry["summary"] = "\n".join(body).strip()
                continue
            ext = f.suffix.lower()
            rel = f"memories/{ydir.name}/{mm}/{f.name}"
            if f.stem.lower() == "cover" and ext in IMG:
                entry["cover"] = rel
            elif ext in AUD:
                entry["audio"] = rel
            elif ext in IMG:
                entry["items"].append({"type": "image", "src": rel, "caption": f.stem})
            elif ext in VID:
                entry["items"].append({"type": "video", "src": rel, "caption": f.stem})
        year[mm] = entry
    if year:
        manifest[ydir.name] = year

out = ROOT / "manifest.json"
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"manifest.json 已生成：{len(manifest)} 个年份")
