import pygame
import json
import sys

# --- 초기화 ---
pygame.init()
screen = pygame.display.set_mode((480, 640))
clock = pygame.time.Clock()
pygame.display.set_caption("리듬게임")

# --- 색상 ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# --- 노트 라인 설정 ---
note_lanes = {
    'd': 60,
    'f': 160,
    'j': 260,
    'k': 360
}

# --- 노트 클래스 ---
class Note:
    def __init__(self, key, time):
        self.key = key
        self.x = note_lanes[key]
        self.y = -50  # 시작 위치
        self.time = time
        self.hit = False

    def update(self, current_time):
        self.y = (current_time - self.time) * 300 + 100

    def draw(self, surface):
        if not self.hit:
            pygame.draw.rect(surface, WHITE, (self.x, self.y, 40, 10))

# --- 음악 & 노트 데이터 로드 ---
pygame.mixer.init()
pygame.mixer.music.load("assets/track1.mp3")
with open("notes/track1.json") as f:
    note_data = json.load(f)

notes = [Note(item["key"], item["time"]) for item in note_data]

# --- 오프셋 설정 ---
offset = 0.0  # 초 단위, 10ms = 0.01초

# --- 게임 시작 ---
pygame.mixer.music.play()
start_ticks = pygame.time.get_ticks()
score = 0
combo = 0

running = True
while running:
    dt = clock.tick(60)
    current_time = (pygame.time.get_ticks() - start_ticks) / 1000 + offset

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                offset -= 0.01  # 10ms 감소
            elif event.key == pygame.K_e:
                offset += 0.01  # 10ms 증가
            else:
                for note in notes:
                    if not note.hit and abs(note.y - 500) < 30:
                        if event.unicode == note.key:
                            note.hit = True
                            score += 100
                            combo += 1
                            break
                else:
                    combo = 0

    screen.fill(BLACK)

    for note in notes:
        note.update(current_time)
        note.draw(screen)

    # 판정선 그리기
    pygame.draw.line(screen, RED, (0, 500), (480, 500), 2)

    # 점수 표시
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    combo_text = font.render(f"Combo: {combo}", True, WHITE)
    offset_text = font.render(f"Offset: {int(offset * 1000)} ms", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(combo_text, (10, 50))
    screen.blit(offset_text, (10, 90))

    pygame.display.flip()

pygame.quit()
sys.exit()
