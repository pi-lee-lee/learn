DROP TABLE IF EXISTS `OrderItems`;
DROP TABLE IF EXISTS `Recipe`;
DROP TABLE IF EXISTS `Inventory`;
DROP TABLE IF EXISTS `OrderList`;
DROP TABLE IF EXISTS `User`;
DROP TABLE IF EXISTS `Part`;
DROP TABLE IF EXISTS `Product`;
DROP TABLE IF EXISTS `CODE`;


CREATE TABLE `CODE` (
  `CODEID` varchar(100) NOT NULL,
  `CODE` varchar(100) DEFAULT NULL,
  `UPPER_CODE` varchar(100) DEFAULT NULL,
  `CODE_NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CODEID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


CREATE TABLE `Inventory` (
  `seq` int(11) NOT NULL AUTO_INCREMENT,
  `I_ID` varchar(100) DEFAULT NULL,
  `QUANTITY` varchar(100) DEFAULT NULL,
  `DATE` datetime DEFAULT NULL,
  PRIMARY KEY (`seq`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

CREATE TABLE `OrderList` (
  `U_ID` varchar(100) DEFAULT NULL,
  `STATE` varchar(100) DEFAULT NULL,
  `ORDER_DATE` datetime DEFAULT NULL,
  `COMP_DATE` datetime DEFAULT NULL,
  `ORDER_ID` varchar(100) NOT NULL,
  PRIMARY KEY (`ORDER_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

CREATE TABLE `Part` (
  `PPID` varchar(100) NOT NULL,
  `NAME` varchar(100) DEFAULT NULL,
  `PRICE` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`PPID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

CREATE TABLE `Product` (
  `PID` varchar(100) NOT NULL,
  `NAME` varchar(100) NOT NULL,
  `PRICE` varchar(100) NOT NULL,
  `DES` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`PID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

CREATE TABLE `Recipe` (
  `P_ID` varchar(100) DEFAULT NULL,
  `PP_ID` varchar(100) DEFAULT NULL,
  `COUNT` int(11) DEFAULT NULL,
  `seq` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`seq`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

CREATE TABLE `User` (
  `IN_ID` varchar(100) NOT NULL,
  `ID` varchar(100) NOT NULL,
  `NAME` varchar(100) NOT NULL,
  `PASS` varchar(100) NOT NULL,
  `CODE` varchar(100) NOT NULL,
  PRIMARY KEY (`IN_ID`),
  UNIQUE KEY `ID` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

CREATE TABLE `OrderItems` (
  `ORDER_ID` varchar(100) DEFAULT NULL,
  `P_ID` varchar(100) DEFAULT NULL,
  `COUNT` varchar(100) DEFAULT NULL,
  KEY `ORDERITEMS_ORDER_ID_IDX` (`ORDER_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 1. CODE 테이블 (사용자 권한 및 주문 상태 공통 코드)
INSERT INTO `CODE` (`CODEID`, `CODE`, `UPPER_CODE`, `CODE_NAME`) VALUES
('CD001', 'AUTH_ADMIN', 'AUTH', '시스템 관리자'),
('CD002', 'AUTH_USER', 'AUTH', '일반 사용자'),
('CD003', 'ORD_RECEIPT', 'ORD_STATE', '주문 접수'),
('CD004', 'ORD_PROCESS', 'ORD_STATE', '제조 중'),
('CD005', 'ORD_COMPLETE', 'ORD_STATE', '배송 완료');

-- 2. User 테이블 (비밀번호 1234 통일, 어드민 포함)
INSERT INTO `User` (`IN_ID`, `ID`, `NAME`, `PASS`, `CODE`) VALUES
('USR001', 'admin', '최관리', '1234', 'CD001'),
('USR002', 'user01', '홍길동', '1234', 'CD002'),
('USR003', 'user02', '김철수', '1234', 'CD002'),
('USR004', 'user03', '이영희', '1234', 'CD002');

-- 3. Part 테이블 (부품 대량 생성 - 12개)
INSERT INTO `Part` (`PPID`, `NAME`, `PRICE`) VALUES
('P001', '인텔 Core i5 CPU', '250000'),
('P002', '인텔 Core i7 CPU', '420000'),
('P003', 'AMD 라이젠 7 CPU', '380000'),
('P004', 'DDR5 16GB RAM', '65000'),
('P005', 'DDR5 32GB RAM', '130000'),
('P006', 'NVMe SSD 1TB', '95000'),
('P007', 'NVMe SSD 2TB', '180000'),
('P008', 'RTX 4060 그래픽카드', '450000'),
('P009', 'RTX 4070 Ti 그래픽카드', '980000'),
('P010', '정격 700W 파워서플라이', '75000'),
('P011', '정격 850W 파워서플라이', '120000'),
('P012', '미들타워 PC 케이스', '60000');

-- 4. Inventory 테이블 (부품 재고 매핑)
INSERT INTO `Inventory` (`I_ID`, `QUANTITY`, `DATE`) VALUES
('P001', '50', NOW()),
('P002', '30', NOW()),
('P003', '40', NOW()),
('P004', '150', NOW()),
('P005', '100', NOW()),
('P006', '80', NOW()),
('P007', '40', NOW()),
('P008', '25', NOW()),
('P009', '15', NOW()),
('P010', '60', NOW()),
('P011', '40', NOW()),
('P012', '70', NOW());

-- 5. Product 테이블 (완제품 대량 생성 - 6개)
INSERT INTO `Product` (`PID`, `NAME`, `PRICE`, `DES`) VALUES
('PROD01', '사무용 가성비 PC', '545000', '문서 작업 및 웹서핑 전용 PC'),
('PROD02', '메인스트림 게이밍 PC', '995000', '가성비 좋은 게이밍 컴퓨터'),
('PROD03', '하이엔드 게이밍 몬스터 PC', '1890000', '고사양 게임 및 영상 편집용 PC'),
('PROD04', 'AMD 원픽 게이밍 PC', '1615000', '원활한 멀티태스킹을 위한 AMD PC'),
('PROD05', '초고속 스토리지 워크스테이션', '1240000', '대용량 파일 작업 전용 컴퓨터'),
('PROD06', '컴팩트 미니 PC', '450000', '공간 활용도가 높은 미니 컴퓨터');

-- 6. Recipe 테이블 (완제품별 소요 부품 매핑 및 수량 설정)
-- auto_increment 컬럼인 seq는 제외하고 입력
INSERT INTO `Recipe` (`P_ID`, `PP_ID`, `COUNT`) VALUES
-- PROD01 (사무용 PC) 구성품
('PROD01', 'P001', 1), -- i5 CPU 1개
('PROD01', 'P004', 1), -- 16GB 램 1개
('PROD01', 'P006', 1), -- 1TB SSD 1개
('PROD01', 'P010', 1), -- 700W 파워 1개
('PROD01', 'P012', 1), -- 케이스 1개
-- PROD02 (메인스트림 게이밍 PC) 구성품
('PROD02', 'P001', 1), -- i5 CPU 1개
('PROD02', 'P004', 2), -- 16GB 램 2개 (총 32G)
('PROD02', 'P006', 1), -- 1TB SSD 1개
('PROD02', 'P008', 1), -- RTX 4060 1개
('PROD02', 'P010', 1), -- 700W 파워 1개
('PROD02', 'P012', 1), -- 케이스 1개
-- PROD03 (하이엔드 게이밍 PC) 구성품
('PROD03', 'P002', 1), -- i7 CPU 1개
('PROD03', 'P005', 2), -- 32GB 램 2개 (총 64G)
('PROD03', 'P007', 1), -- 2TB SSD 1개
('PROD03', 'P009', 1), -- RTX 4070 Ti 1개
('PROD03', 'P011', 1), -- 850W 파워 1개
('PROD03', 'P012', 1); -- 케이스 1개

-- 7. OrderList 테이블 (주문 마스터 데이터)
INSERT INTO `OrderList` (`U_ID`, `STATE`, `ORDER_DATE`, `COMP_DATE`, `ORDER_ID`) VALUES
('USR002', 'CD005', '2026-07-20 10:00:00', '2026-07-22 15:00:00', 'ORD20260720-001'),
('USR003', 'CD004', '2026-07-30 11:30:00', NULL,                  'ORD20260730-001'),
('USR004', 'CD003', '2026-07-31 14:15:00', NULL,                  'ORD20260731-001');

-- 8. OrderItems 테이블 (주문별 상세 완제품 및 주문 수량)
INSERT INTO `OrderItems` (`ORDER_ID`, `P_ID`, `COUNT`) VALUES
('ORD20260720-001', 'PROD01', '2'), -- 홍길동이 사무용 PC 2대 주문 완료
('ORD20260730-001', 'PROD03', '1'), -- 김철수가 하이엔드 PC 1대 주문 (제조 중)
('ORD20260731-001', 'PROD02', '1'), -- 이영희가 게이밍 PC 1대 주문 (접수 상태)
('ORD20260731-001', 'PROD06', '3'); -- 이영희가 미니 PC 3대 함께 주문 (접수 상태)
