"""check_script.py – lint a script.json against the retention rules in GO.md §15/§18 before any TTS quota is spent.
usage: python3 check_script.py <script.json>     exit code 1 = at least one FAIL (WARN never fails)."""
import json, re, sys
L = json.load(open(sys.argv[1])); fails = 0
def words(s): return re.findall(r"[\wäöüÄÖÜß.\-%]+", s)
def say(level, msg):
    global fails; fails += level == "FAIL"; print(f"{level:4} {msg}")
hook = L[0]["say"]; hw = words(hook)
if len(hw) > 7: say("FAIL", f"hook has {len(hw)} words (max 7): {hook}")
if re.match(r"\s*(mal angenommen|hallo|hey|hi|willkommen|heute)\b", hook.lower()): say("FAIL", "hook starts with a greeting / 'Mal angenommen'")
if len(L[0]["show"]) > 48: say("WARN", f"hook text has {len(L[0]['show'])} characters – the big card on frame 0 reads best under 48")
total = sum(len(words(l["say"])) for l in L)
if not 55 <= total <= 70: say("WARN" if 50 <= total <= 75 else "FAIL", f"{total} words (target 55–70 = 20–25 s)")
for i, l in enumerate(L):
    for s in re.split(r"(?<=[.?!])\s+", l["say"]):
        if len(words(s)) > 12: say("WARN", f"line {i}: sentence with {len(words(s))} words (aim ≤ 10): {s}")
    if re.search(r"\d", l["say"]): say("FAIL", f"line {i}: digits in 'say' – spell numbers out (digits belong in 'show')")
    if len(words(l["say"])) > 19: say("WARN", f"line {i}: {len(words(l['say']))} words in one scene (> 19 = picture stands too long)")
    if "scene" not in l or "show" not in l: say("FAIL", f"line {i}: needs say, show, scene")
if not 5 <= len(L) <= 8: say("WARN", f"{len(L)} scenes (usual: 6–7)")
if re.search(r"schick (das|es|'s|’s)", L[-1]["say"].lower()): say("WARN", "ending is a share persona – allowed at most every 3rd video (check the log in GO.md §15)")
print(f"hook: {len(hw)} words | total: {total} words | scenes: {len(L)} | {'FAILED' if fails else 'ok'}"); sys.exit(1 if fails else 0)
