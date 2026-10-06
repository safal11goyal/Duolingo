import urllib.request
import json

BASE = "http://127.0.0.1:8000"

def post(path, body={}):
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def get(path):
    with urllib.request.urlopen(f"{BASE}{path}") as resp:
        return json.loads(resp.read().decode("utf-8"))

print("=== 1. Check Me ===")
me = get("/api/me")
print(f"User: {me['username']}, XP: {me['xp']}, Hearts: {me['hearts']}, Streak: {me['streak']}")

print("\n=== 2. Check Learning Path ===")
path = get("/api/path")
print(f"Course: {path['course_name']} ({path['source_language']} -> {path['target_language']})")
for u in path["units"]:
    print(f" - {u['title']}: {len(u['skills'])} skills")

print("\n=== 3. Start Lesson 1 ===")
start = post("/api/lessons/1/start")
print(f"Attempt ID: {start['attempt_id']}, Hearts: {start['hearts_remaining']}, Exercises: {start['total_exercises']}")

print("\n=== 4. Submit Correct Answer ===")
ans1 = post("/api/lessons/1/answer", {"exercise_id": 1, "answer": "Hola", "attempt_id": start["attempt_id"]})
print(f"Correct: {ans1['correct']}, +XP: {ans1['xp_earned']}, Hearts Remaining: {ans1['hearts_remaining']}")

print("\n=== 5. Submit Wrong Answer (Hearts deduction) ===")
ans2 = post("/api/lessons/1/answer", {"exercise_id": 1, "answer": "Wrong Answer", "attempt_id": start["attempt_id"]})
print(f"Correct: {ans2['correct']}, +XP: {ans2['xp_earned']}, Hearts Remaining: {ans2['hearts_remaining']}")

print("\n=== 6. Complete Lesson ===")
comp = post("/api/lessons/1/complete", {"attempt_id": start["attempt_id"]})
print(f"Success: {comp['success']}, Bonus XP: {comp['xp_earned']}, Total XP: {comp['total_xp']}, Streak: {comp['streak']}, Next Unlocked: {comp['next_skill_unlocked']}")

print("\n=== 7. Check Profile & Leaderboard ===")
profile = get("/api/profile")
print(f"Profile: Crowns: {profile['crowns_count']}, League: {profile['league']}, Rank: #{profile['rank']}")
lb = get("/api/leaderboard")
print(f"Leaderboard top 3: {[u['display_name'] for u in lb[:3]]}")
