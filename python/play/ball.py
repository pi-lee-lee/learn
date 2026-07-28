import tkinter as tk
import math
import random

class Ball:
    # 모든 공 객체가 실시간으로 공유할 마찰계수 초기값 (클래스 변수)
    floor_friction = 0.993
    floor_spin_drag = 0.985
    # --- [새로 분리된 수평 회전 전용 바닥 마찰 계수] ---
    floor_horizontal_spin_drag = 0.9985  # 저항을 크게 줄여 스핀이 오래 유지되도록 설정

    def __init__(self, canvas, x, y, vx, vy, omega_z, omega_t, radius=30, color="orange"):
        self.canvas = canvas
        self.radius = radius
        self.m = 1.0       # 질량
        
        # 위치 및 선속도
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        
        # [독립된 2가지 회전 상태]
        self.omega_z = omega_z   # 1. 수평 회전 (Z축 팽이 스핀, 라디안)
        self.omega_t = omega_t   # 2. 수직 회전 (이동 방향 구름 스핀, 라디안)
        
        self.angle_z = 0.0       # 수평 회전각
        self.angle_t = 0.0       # 수직 회전각
        
        # 물리 계수
        self.e = 0.95            # 벽/공 충돌 반발 계수 (입사각/반사각 보장)
        self.mu = 0.25           # 충돌 시 속도 <-> 회전 전환 마찰계수
        self.mu_floor = 0.15     # 바닥 미끄러짐(Sliding) 동마찰계수

        # 시각화 위젯 생성 (공 본체 + 수평 회전선 2개 + 수직 구름 표시용 점)
        self.body = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline="black", width=2)
        self.line1 = canvas.create_line(x, y, x, y, fill="black", width=2)
        self.line2 = canvas.create_line(x, y, x, y, fill="black", width=2)
        self.dot = canvas.create_oval(x-4, y-4, x+4, y+4, fill="white", outline="black")
        self.update_view()

    def update_position(self):
        # 1. 선속도에 의한 위치 이동
        self.x += self.vx
        self.y += self.vy
        
        # 2. 회전각 업데이트 (수평 및 수직)
        self.angle_z += self.omega_z
        self.angle_t += self.omega_t
        
        # 3. [수직 구름 물리] 바닥 미끄러짐과 수직 회전의 상호 전이
        v_speed = math.hypot(self.vx, self.vy)
        v_slip_floor = v_speed - self.radius * self.omega_t
        
        if v_speed > 0.05 and abs(v_slip_floor) > 0.05:
            # 바닥과의 마찰로 미끄러짐이 있으면 선속도와 수직 회전이 서로 에너지를 교환
            jt_floor = (2/7) * self.m * v_slip_floor
            max_jt_floor = self.mu_floor * self.m * 9.8 * 0.016
            jt_floor = max(-max_jt_floor, min(max_jt_floor, jt_floor))
            
            # 속도 방향 벡터 성분 분해 후 감속/가속 적용
            nx_move, ny_move = self.vx / v_speed, self.vy / v_speed
            self.vx -= (jt_floor / self.m) * nx_move
            self.vy -= (jt_floor / self.m) * ny_move
            self.omega_t += (2.5 * jt_floor) / (self.m * self.radius)
        elif v_speed > 0.05:
            # 순수 구름 상태(Pure Rolling): 수직 회전이 선속도와 완벽히 동기화되어 고정
            self.omega_t = v_speed / self.radius

        # 4. 실시간 바닥 마찰 저항 적용
        self.vx *= Ball.floor_friction
        self.vy *= Ball.floor_friction
        self.omega_t *= Ball.floor_spin_drag          # 수직 구름 마찰은 기존 저항 유지
        self.omega_z *= Ball.floor_horizontal_spin_drag # 수평 팽이 스핀 마찰은 매우 미미하게 감소

        # 미세 진동 및 흐름 방지 멈춤 처리
        if math.hypot(self.vx, self.vy) < 0.05:
            self.vx, self.vy, self.omega_t = 0, 0, 0
        if abs(self.omega_z) < 0.001:
            self.omega_z = 0

        self.update_view()

    def resolve_wall_collision(self, width, height):
        # 1. 좌우 벽 충돌
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            if self.x - self.radius <= 0:
                self.x = self.radius
                nx, ny = 1.0, 0.0
            else:
                self.x = width - self.radius
                nx, ny = -1.0, 0.0
            
            tx, ty = -ny, nx
            v_n = self.vx * nx + self.vy * ny
            v_t = self.vx * tx + self.vy * ty

            jn = self.m * (1 + self.e) * abs(v_n)
            
            # 수평 회전(omega_z)이 벽면 접선 속도와 맞물림
            v_slip = v_t - self.radius * self.omega_z
            jt = (2/7) * self.m * v_slip
            
            max_jt = self.mu * jn
            jt = max(-max_jt, min(max_jt, jt))

            v_t_new = v_t - jt / self.m
            v_n_new = -self.e * v_n

            self.vx = v_n_new * nx + v_t_new * tx
            self.vy = v_n_new * ny + v_t_new * ty
            self.omega_z += (2.5 * jt) / (self.m * self.radius)
            self.omega_t *= -self.e 

        # 2. 상하 벽 충돌
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            if self.y - self.radius <= 0:
                self.y = self.radius
                nx, ny = 0.0, 1.0
            else:
                self.y = height - self.radius
                nx, ny = 0.0, -1.0
            
            tx, ty = -ny, nx
            v_n = self.vx * nx + self.vy * ny
            v_t = self.vx * tx + self.vy * ty

            jn = self.m * (1 + self.e) * abs(v_n)
            v_slip = v_t - self.radius * self.omega_z
            jt = (2/7) * self.m * v_slip
            
            max_jt = self.mu * jn
            jt = max(-max_jt, min(max_jt, jt))

            v_t_new = v_t - jt / self.m
            v_n_new = -self.e * v_n

            self.vx = v_n_new * nx + v_t_new * tx
            self.vy = v_n_new * ny + v_t_new * ty
            self.omega_z += (2.5 * jt) / (self.m * self.radius)
            self.omega_t *= -self.e

    def update_view(self):
        # 본체 동기화
        self.canvas.coords(self.body, self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)
        
        # 수평 회전(Z축 십자선) 시각화 계산
        cos_z = math.cos(self.angle_z) * self.radius
        sin_z = math.sin(self.angle_z) * self.radius
        self.canvas.coords(self.line1, self.x - cos_z, self.y - sin_z, self.x + cos_z, self.y + sin_z)
        self.canvas.coords(self.line2, self.x + sin_z, self.y - cos_z, self.x - sin_z, self.y + cos_z)
        
        # 수직 회전(구름 진행률 점) 시각화 계산
        v_speed = math.hypot(self.vx, self.vy)
        if v_speed > 0:
            dx, dy = self.vx / v_speed, self.vy / v_speed
        else:
            dx, dy = 1.0, 0.0
        
        dot_r = self.radius * 0.6 * math.cos(self.angle_t)
        dot_x = self.x + dx * dot_r
        dot_y = self.y + dy * dot_r
        self.canvas.coords(self.dot, dot_x - 4, dot_y - 4, dot_x + 4, dot_y + 4)

def resolve_ball_collision(b1, b2):
    dx = b2.x - b1.x
    dy = b2.y - b1.y
    dist = math.hypot(dx, dy)
    min_dist = b1.radius + b2.radius
    
    if dist >= min_dist: return

    # 위치 중첩 보정
    overlap = min_dist - dist
    nx, ny = dx / dist, dy / dist
    b1.x -= nx * overlap * 0.5
    b1.y -= ny * overlap * 0.5
    b2.x += nx * overlap * 0.5
    b2.y += ny * overlap * 0.5

    tx, ty = -ny, nx

    # 선속도 분해
    v1n, v1t = b1.vx * nx + b1.vy * ny, b1.vx * tx + b1.vy * ty
    v2n, v2t = b2.vx * nx + b2.vy * ny, b2.vx * tx + b2.vy * ty

    # 1. 수직 탄성 충돌 충격량 (입사/반사 보장)
    e = min(b1.e, b2.e)
    jn = (b1.m * b2.m * (1 + e) * (v2n - v1n)) / (b1.m + b2.m)
    
    # 2. 접촉면 수평 스핀(omega_z) 변환 충격량 계산
    v_slip_z = (v1t - b1.radius * b1.omega_z) - (v2t + b2.radius * b2.omega_z)
    jt = v_slip_z / ((7 / (2 * b1.m)) + (7 / (2 * b2.m)))
    
    mu = (b1.mu + b2.mu) / 2
    max_jt = mu * abs(jn)
    jt = max(-max_jt, min(max_jt, jt))

    # 접선 선속도 및 수평 회전 속도 수정
    v1t_new = v1t - jt / b1.m
    v2t_new = v2t + jt / b2.m
    v1n_new = v1n + jn / b1.m
    v2n_new = v2n - jn / b2.m

    b1.omega_z += (2.5 * jt) / (b1.m * b1.radius)
    b2.omega_z += (2.5 * jt) / (b2.m * b2.radius)

    # 3. 두 공 충돌 시 수직 회전(omega_t)의 반사 전이
    b1.omega_t *= -e
    b2.omega_t *= -e

    # 최종 운동량 벡터 대입
    b1.vx = v1n_new * nx + v1t_new * tx
    b1.vy = v1n_new * ny + v1t_new * ty
    b2.vx = v2n_new * nx + v2t_new * tx
    b2.vy = v2n_new * ny + v2t_new * ty

# --- 메인 윈도우 및 컨트롤 패널 구성 ---
WIDTH, HEIGHT = 700, 500
window = tk.Tk()
window.title("수평 회전 저항이 최적화된 통합 시뮬레이션")

control_frame = tk.Frame(window)
control_frame.pack(fill=tk.X, side=tk.TOP, padx=10, pady=5)

def spawn_random_ball():
    radius = random.randint(25, 35)
    x = random.randint(radius + 10, WIDTH - radius - 10)
    y = random.randint(radius + 10, HEIGHT - radius - 10)
    vx = random.uniform(-10, 10)
    vy = random.uniform(-10, 10)
    
    # 강력한 수평 스핀(omega_z)과 임의의 수직 구름 스핀(omega_t) 부여
    omega_z = random.uniform(-1.2, 1.2) 
    omega_t = random.uniform(-0.8, 0.8) 
    
    color = random.choice(["orange", "cyan", "magenta", "yellow", "lime", "red", "dodgerblue"])
    balls.append(Ball(canvas, x, y, vx, vy, omega_z, omega_t, radius=radius, color=color))

spawn_btn = tk.Button(control_frame, text="강력 스핀 공 생성 ⚾", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", command=spawn_random_ball)
spawn_btn.pack(side=tk.LEFT, padx=10)

# 마찰력 제어 슬라이더 연결
def update_friction(val):
    slider_val = float(val)
    # 바닥 마찰력 조절 (선속도와 수직 회전에만 영향)
    Ball.floor_friction = 1.0 if slider_val == 100 else 0.90 + (slider_val / 1000)
    Ball.floor_spin_drag = 1.0 if slider_val == 100 else 0.85 + (slider_val / 666)

f_frame = tk.Frame(control_frame)
f_frame.pack(side=tk.LEFT, padx=15)
tk.Label(f_frame, text="바닥 마찰력 (슬라이더 조작)", font=("Arial", 9)).pack()
friction_scale = tk.Scale(f_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=150, command=update_friction)
friction_scale.set(93)
friction_scale.pack()

canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

balls = []
spawn_random_ball()

def game_loop():
    for ball in balls:
        ball.update_position()
    for ball in balls:
        ball.resolve_wall_collision(WIDTH, HEIGHT)
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            resolve_ball_collision(balls[i], balls[j])
            
    window.after(16, game_loop)

game_loop()
window.mainloop()
