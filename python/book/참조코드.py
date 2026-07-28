import time
import sys
import random

# 터미널 제어 문자 정의
CLEAN_SCREEN = "\033[2J"    # 화면 전체 청소
RESET_CURSOR = "\033[1;1H"    # 커서를 1행 1열(맨 위)로 이동
HIDE_CURSOR  = "\033[?25l"    # 깜빡이는 커서 숨기기
SHOW_CURSOR  = "\033[?25h"    # 커서 다시 보이기

# 보드 구성에 사용할 이모지 블록 정의
BLOCKS = {
    "WALL": "⬛", "EMPTY": "⬜", 
    "Y": "🟨", "G": "🟩", "B": "🟦", "P": "🟪"
}

def generate_board_string(loop_count):
    """
    10x20 구조의 보드 문자열을 동적으로 생성합니다.
    내부 '⬜' 공간에 실시간 변화(예: 테트리스 블록이 떨어지는 연출)를 추가할 수 있습니다.
    """
    lines = []
    
    # 총 20개의 행(Row) 생성
    for row in range(20):
        # 1. 왼쪽 벽과 플레이 필드 (기본 ⬜, 특정 조건에서 랜덤 블록 노출 예시)
        left_wall = BLOCKS["WALL"]
        
        # 실시간 변화를 시각적으로 보여주기 위한 임시 연출 코드 (블록 낙하 흉내)
        field = ""
        for col in range(10):
            if row == (loop_count % 20) and col in (4, 5): 
                field += BLOCKS["Y"] # 현재 루프 위치에 노란 블록 배치
            else:
                field += BLOCKS["EMPTY"]
                
        # 2. 중간 벽
        mid_wall = BLOCKS["WALL"]
        
        # 3. 오른쪽 대기열 / 스코어 영역 (🟨🟩🟦🟪)
        # 이 영역도 고정해 두거나 인덱스에 따라 변화를 줄 수 있습니다.
        next_queue = BLOCKS["Y"] + BLOCKS["G"] + BLOCKS["B"] + BLOCKS["P"]
        
        # 한 줄 완성
        full_line = f"{left_wall}{field}{mid_wall}{next_queue}"
        lines.append(full_line)
        
    # 모든 줄을 줄바꿈 문자(\n)로 엮어서 하나의 거대한 문자열 스냅샷으로 반환
    return "\n".join(lines)


def main_loop():
    try:
        # 최초 1회 화면을 완전히 청소하고 커서를 숨깁니다.
        sys.stdout.write(CLEAN_SCREEN)
        sys.stdout.write(HIDE_CURSOR)
        
        loop = 0
        while True:
            # 1. 커서를 터미널 맨 위로 강제 이동
            sys.stdout.write(RESET_CURSOR)
            
            # 2. 현재 상태의 보드 모양 획득 및 출력
            board_snapshot = generate_board_string(loop)
            sys.stdout.write(board_snapshot)
            sys.stdout.write(f"\n\n[ Frame Count: {loop} ]") # 상태창 분리
            
            # 3. 터미널 버퍼 비우기 (즉시 반영)
            sys.stdout.flush()
            
            loop += 1
            time.sleep(0.1) # 0.1초마다 프레임 업데이트 (10 FPS)
            
    except KeyboardInterrupt:
        # Ctrl + C를 눌러 프로그램을 종료할 때 커서를 원래대로 복구합니다.
        sys.stdout.write(SHOW_CURSOR)
        print("\n\n👋 프로그램을 종료합니다.")

if __name__ == "__main__":
    main_loop()
