from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from datetime import datetime

class TCon(Session):
    def execute(self, statement, params=None, *args, **kwargs):

        sql_text = ""
        if hasattr(statement, "text"):
            sql_text = statement.text  # text("SELECT...") 형태일 때
        elif isinstance(statement, str):
            sql_text = statement       # 생 문자열일 때
            statement = text(statement) # SQLAlchemy 실행 호환을 위해 래핑

        is_write = any(sql_text.strip().upper().startswith(cmd) for cmd in ["INSERT", "UPDATE", "DELETE"])

        if is_write and not self.in_transaction():
            print(f"[트랜잭션 자동 시작]")
            self.begin()
            
        try:
            return super().execute(statement, params, *args, **kwargs)
            
        except SQLAlchemyError as e:
            if self.in_transaction():
                self.rollback()
                print(f"[자동 롤백 완료] SQL 실행 오류로 트랜잭션이 취소되었습니다.")
            print(f"[DB 에러 상세]: {e}")
            raise e
            
        except Exception as e:
            if self.in_transaction():
                self.rollback()
            print(f"[시스템 에러 발생]: {e}")
            raise e

    def commit(self):
        try:
            super().commit()
        except SQLAlchemyError as e:
            super().rollback()
            print(f"[커밋 에러] 최종 반영 중 오류 발생으로 롤백됨: {e}")
            raise e


class DBmng:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_url: str = "mysql+mysqldb://test:1234@127.0.0.1:3306/aitest"):
        if hasattr(self, 'initialized'): 
            return
        
        self.engine = create_engine(
            db_url,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=1800
        )
        
        self.SessionLocal = sessionmaker(
            class_=TCon, 
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )
        self.initialized = True

    def get_connection(self) -> TCon:
        return self.SessionLocal()



# 단위테스트
if __name__ == "__main__":
    
    db_manager = DBmng()

    db1 = None
    db2 = None

    try:
        db1 = db_manager.get_connection()
        db2 = db_manager.get_connection()

        print("db1, db2 커넥션 생성 완료. 각각의 쿼리 수행 시작...")

        
        result = db1.execute(text('select * from Customers'))

        

        query  = f"INSERT INTO Customers (Name, Email, JoinDate, City, Age, Phone) VALUES ('남남남', 'k@a.com', '{ datetime.now().strftime('%Y-%m-%d')}', '영월군', 41, '063-889-1065')"

        #트랜젝션 시작
        db2.execute(text(query))
        db2.commit()
                
        print("동시 작업 완료 처리 진행")

    except Exception as error:
        print(f"작업 진행 중 예상치 못한 에러 발생: {error}")
        
    finally:
        if db1:
            db1.close()
            print("db1 커넥션 반납 완료")
            
        if db2:
            db2.close()
            print("db2 커넥션 커밋 및 반납 완료")