#include <iostream>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <memory>
#include <io.h>
#include <fcntl.h>
#include <mariadb/mysql.h>
#include <windows.h> 

using namespace std;

class MariaDBPool {
private:

    queue<MYSQL*> pool;
    mutex mtx;
    condition_variable cv;
    
    // DB 접속 정보 변수
    string host, user, password, dbname;
    unsigned int port;
    size_t poolSize;

    // 싱글톤 구현을 위한 프라이빗 생성자
    MariaDBPool() : port(3306), poolSize(5) {}

    // 새로운 실제 커넥션을 생성하는 헬퍼 함수
    MYSQL* createConnection() {
        MYSQL* conn = mysql_init(nullptr);
        if (!conn) return nullptr;

        // 💡 윈도우 Clang 터미널 환경과의 한글 싱크를 위해 UTF-8 연결 세팅 주입
        mysql_options(conn, MYSQL_SET_CHARSET_NAME, "utf8mb4");


        if (!mysql_real_connect(conn, host.c_str(), user.c_str(), password.c_str(), dbname.c_str(), port, nullptr, 0)) {
            cerr << "DB 연결 실패: " << mysql_error(conn) << endl;
            mysql_close(conn);
            return nullptr;
        }

        mysql_set_character_set(conn, "utf8mb4");
        return conn;
    }

public:
    // 싱글톤 인스턴스 획득
    static MariaDBPool& getInstance() {
        static MariaDBPool instance;
        return instance;
    }

    // 풀 초기화 및 커넥션 사전 채우기
    bool init(string h, string u, string p, string db, unsigned int pt, size_t size) {
        lock_guard<mutex> lock(mtx);
        host = h; user = u; password = p; dbname = db; port = pt; poolSize = size;

        for (size_t i = 0; i < poolSize; ++i) {
            MYSQL* conn = createConnection();
            if (conn) {
                pool.push(conn);
            } else {
                return false; // 하나라도 실패하면 초기화 실패 처리
            }
        }
        return true;
    }

    // 풀에서 커넥션 하나 꺼내기 (스레드 세이프)
    MYSQL* getConnection() {
        unique_lock<mutex> lock(mtx);
        // 풀이 비어있으면 자원이 반납될 때까지 스레드를 대기시킵니다.
        cv.wait(lock, [this] { return !pool.empty(); });

        MYSQL* conn = pool.front();
        pool.pop();
        return conn;
    }

    // 사용이 끝난 커넥션을 풀에 반납하기
    void releaseConnection(MYSQL* conn) {
        if (!conn) return;
        lock_guard<mutex> lock(mtx);
        pool.push(conn);
        cv.notify_one(); // 대기 중인 다른 스레드에게 알림
    }

    // 프로그램 종료 시 전체 풀 자원 해제
    ~MariaDBPool() {
        lock_guard<mutex> lock(mtx);
        while (!pool.empty()) {
            mysql_close(pool.front());
            pool.pop();
        }
    }

    // 복사 방지
    MariaDBPool(const MariaDBPool&) = delete;
    MariaDBPool& operator=(const MariaDBPool&) = delete;
};

// 💡 RAII 패턴을 적용하여 사용자가 수동으로 반납하지 않아도 자동으로 소멸 시 풀에 들어가는 래퍼 클래스
class [[nodiscard]] DBConnectionGuard {
private:
    MYSQL* conn;
public:
    DBConnectionGuard() { conn = MariaDBPool::getInstance().getConnection(); }
    ~DBConnectionGuard() { MariaDBPool::getInstance().releaseConnection(conn); }
    MYSQL* get() const { return conn; }
};

int main() {
    // Clang 통합 터미널 한글 출력 안정화
    SetConsoleOutputCP(CP_UTF8);
    // 1. 커넥션 풀 초기화 (본인의 실제 DB 정보로 수정 필수)
    bool success = MariaDBPool::getInstance().init("127.0.0.1", "test", "1234", "aitest", 3306, 3);
    
    if (!success) {
        cout << "마리아디비 커넥션 풀 빌드 실패 ❌" << endl;
        return 1;
    }
    cout << "마리아디비 커넥션 풀 생성 성공! 🚀" << endl;

    {
        // 2. 풀에서 커넥션 획득
        DBConnectionGuard db;
        MYSQL* my_conn = db.get();

        if (my_conn) {
            cout << "\n--- Product 테이블 조회 시작 ---" << endl;
            
            // 💡 3. 실행할 쿼리문 정의
            const char* query = "SELECT * FROM Product p";
            
            // 💡 4. 쿼리 전송 (성공 시 0을 반환합니다)
            if (mysql_query(my_conn, query)) {
                cerr << "쿼리 실행 실패: " << mysql_error(my_conn) << endl;
            } else {
                // 💡 5. 서버로부터 결과 메모리에 로드
                MYSQL_RES* res = mysql_store_result(my_conn);
                if (res == nullptr) {
                    // 결과 집합이 없는 쿼리(INSERT/UPDATE 등)이거나 에러인 경우
                    if (mysql_field_count(my_conn) == 0) {
                        cout << "조회된 데이터가 없습니다." << endl;
                    } else {
                        cerr << "결과 가져오기 실패: " << mysql_error(my_conn) << endl;
                    }
                } else {
                    // 💡 6. 데이터 추출 및 화면 출력 루프
                    MYSQL_ROW row;
                    unsigned int num_fields = mysql_num_fields(res); // 컬럼 개수 확인
                    
                    int row_count = 1;
                    while ((row = mysql_fetch_row(res))) {
                        cout << "[" << row_count++ << "] ";
                        
                        // 한 행의 모든 컬럼 값을 순서대로 출력
                        for (unsigned int i = 0; i < num_fields; i++) {
                            // 데이터가 NULL인 경우를 대비한 안전 조치
                            cout << (row[i] ? row[i] : "NULL");
                            
                            // 컬럼 사이에 구분자 추가
                            if (i < num_fields - 1) cout << " | ";
                        }
                        cout << "\n";
                    }
                    
                    // 💡 7. 결과 집합 메모리 해제 (필수)
                    mysql_free_result(res);
                }
            }
            cout << "--- Product 테이블 조회 종료 ---\n" << endl;
        }
    } // 8. 블록을 빠져나가며 커넥션 자동 반납

    cout << "자원이 풀에 안전하게 반납되었습니다." << endl;
    std::system("pause"); 

    return 0;
}
