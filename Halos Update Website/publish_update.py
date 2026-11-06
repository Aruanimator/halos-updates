"""Adds a new Halos version to latest.json (the file every installed Halos checks).

usage:
  python3 publish_update.py 1.4.1 "Faster Magic Layers" "Fixed captions on Mac" \
      --win https://github.com/<you>/halos-updates/releases/download/v1.4.1/Halos.1.4.1.Update.exe \
      --mac https://github.com/<you>/halos-updates/releases/download/v1.4.1/Halos.1.4.1.Update.pkg \
      --win-file "Halos 1.4.1 Update.exe" --mac-file "Halos 1.4.1 Update.pkg"

Then upload the site folder again (Cloudflare Pages: drag the folder onto the project's
"Upload assets" page). Every Halos that's open sees the update within a day, or at once with "Check now".
"""
import argparse, datetime, json, os

here = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("version")
ap.add_argument("notes", nargs="*")
ap.add_argument("--win", default="")
ap.add_argument("--mac", default="")
ap.add_argument("--win-file", default="", help="local update .exe, to record its size")
ap.add_argument("--mac-file", default="", help="local update .pkg, to record its size")
a = ap.parse_args()

path = os.path.join(here, "latest.json")
m = json.load(open(path)) if os.path.exists(path) else {"history": []}
today = datetime.date.today().isoformat()
size = lambda f: os.path.getsize(f) if f and os.path.exists(f) else 0
m.update({
    "version": a.version, "date": today, "notes": a.notes or ["Improvements and fixes"],
    "win": {"url": a.win, "size": size(a.win_file)},
    "mac": {"url": a.mac, "size": size(a.mac_file)},
})
hist = [h for h in m.get("history", []) if h.get("version") != a.version]
m["history"] = [{"version": a.version, "date": today, "notes": m["notes"]}] + hist
json.dump(m, open(path, "w"), indent=2)
print("latest.json now offers Halos", a.version)
