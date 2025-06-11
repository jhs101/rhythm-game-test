import json

print("🎼 4키 리듬게임 노트 자동 생성기")

# --- 사용자 입력 받기 ---
track_name = input("노트 파일 이름 (예: track1): ").strip()
bpm = float(input("BPM 입력: "))
start_beat = float(input("시작 박자 (예: 0): "))
end_beat = float(input("끝 박자 (예: 32): "))
pattern = input("패턴 문자열 (예: d-j-f-k-d---j---): ").strip().replace(' ', '')

# --- 계산 ---
beat_duration = 60.0 / bpm  # 1박의 길이 (초)
note_data = []

for i, key in enumerate(pattern):
    if key in ['d', 'f', 'j', 'k']:
        time = (start_beat + i) * beat_duration
        note_data.append({"time": round(time, 3), "key": key})

# --- 저장 ---
filename = f"notes/{track_name}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(note_data, f, indent=2)

print(f"✅ 생성 완료: {filename}")
