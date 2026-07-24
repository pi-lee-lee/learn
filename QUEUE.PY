import threading
import queue
import time
import random

# 1. 환경 설정
NUM_THREADS = 30
TOTAL_DATA_COUNT = 500

# 30개의 스레드별 작업 큐 생성 (리스트로 관리)
task_queues = [queue.Queue() for _ in range(NUM_THREADS)]

# 모든 스레드가 결과를 안전하게 담을 공통 결과 큐 (Thread-safe)
result_queue = queue.Queue()

# 2. 스레드가 수행할 무한 루프 작업 함수
def worker_task(worker_id, my_queue):
    while True:
        # 큐에서 데이터를 가져옴 (데이터가 없으면 들어올 때까지 무한 대기)
        task_packet = my_queue.get()
        
        # 종료 신호(None)를 받으면 루프 탈출
        if task_packet is None:
            my_queue.task_done()
            break
            
        # 패킷 분해: 작업 일련번호(0~499)와 실제 데이터
        task_id, data = task_packet
        
        # [실제 작업 수행 공간] (예시: 랜덤 대기로 완료 순서 꼬이게 만듦)
        time.sleep(random.uniform(0.01, 0.05)) 
        processed_result = f"★ {data} 처리 완료 (by 스레드-{worker_id})"
        
        # 결과를 [작업 일련번호]와 함께 결과 큐에 투척
        result_queue.put((task_id, processed_result))
        
        # 큐 작업 완료 알림
        my_queue.task_done()

# 3. 30개의 백그라운드 스레드 생성 및 시작
threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=worker_task, args=(i, task_queues[i]))
    t.daemon = True # 메인 프로그램 종료 시 함께 종료되도록 설정
    threads.append(t)
    t.start()

# 4. 메인 스레드: 500개의 작업 데이터를 30개 큐에 분배 입력 (Round-Robin 방식)
print("=== 메인 스레드: 500개 작업 데이터 큐 입력 시작 ===")
for task_id in range(TOTAL_DATA_COUNT):
    raw_data = f"{task_id}번 데이터"
    
    # 30개의 큐에 순서대로 하나씩 골고루 나눕니다. (0번 큐, 1번 큐 ... 29번 큐 -> 다시 0번 큐)
    target_queue_idx = task_id % NUM_THREADS
    
    # 중요: (일련번호, 데이터) 튜플 형태로 입력하여 순서 값을 유지합니다.
    task_queues[target_queue_idx].put((task_id, raw_data))

# 5. 메인 스레드: 모든 작업 큐가 빌 때까지 대기 (join)
for q in task_queues:
    q.join()

print("=== 모든 스레드 작업 완료! 데이터 정렬 시작 ===")

# 6. 결과 큐에서 데이터를 모두 꺼내어 리스트로 변환
unsorted_results = []
while not result_queue.empty():
    unsorted_results.append(result_queue.get())

# 7. [핵심] 작업 일련번호(item[0])를 기준으로 오름차순 정렬
# lambda를 사용하여 튜플의 첫 번째 요소인 task_id 기준으로 정렬합니다.
unsorted_results.sort(key=lambda item: item[0])

# 정렬된 순수 결과물만 추출
final_ordered_results = [result for task_id, result in unsorted_results]

# 8. 최종 결과 확인 출력 (0번부터 499번까지 지시 순서대로 완벽히 정렬됨)
print("\n=== 최종 정렬된 결과물 (일부 출력) ===")
for idx in range(500): # 상위 10개만 출력 확인
    print(f"[지시순서 {idx}] -> {final_ordered_results[idx]}")

# 9. (선택사항) 무한 루프 스레드들을 안전하게 완전 종료하고 싶을 때 신호 전달
for q in task_queues:
    q.put(None)
