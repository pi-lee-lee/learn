import os
import time
import sys

CLEAN_SCREEN = "\033[2J"    # 화면 전체 청소
RESET_CURSOR = "\033[1;1H"    # 커서를 1행 1열(맨 위)로 이동
HIDE_CURSOR  = "\033[?25l"    # 깜빡이는 커서 숨기기
SHOW_CURSOR  = "\033[?25h"    # 커서 다시 보이기

sys.stdout.write(CLEAN_SCREEN)
sys.stdout.write(HIDE_CURSOR)

time
for i in range(100):
    sys.stdout.write("\033[1;1H")
    print('⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟩🟦🟪') 
    print('⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟩🟦🟪') 
    print('⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟩🟦🟪') 
    print('⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟩🟦🟪') 
    print('⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟩🟦🟪') 
    print('⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟩🟦🟪') 
    print('⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟩🟦🟪')
    
    time.sleep(0.1)

sys.stdout.write(SHOW_CURSOR)