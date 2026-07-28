import dis

def test_func():
    a = 10
    b = 0
    result = a / b  # 에러 발생 지점

try:
    test_func()
except Exception as e:
    tb = e.__traceback__

    while tb.tb_next != None :
        tb = tb.tb_next


    # 1단계 내부(test_func)의 traceback으로 이동
    inner_tb = tb 
    
    print(f"에러 소스 라인 (tb_lineno): {inner_tb.tb_lineno}")
    print(f"에러 바이트코드 인덱스 (tb_lasti): {inner_tb.tb_lasti}")

    
    print("\n--- 실제 바이트코드 구조 ---")
    dis.dis(test_func)