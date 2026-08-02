-- ==========================================================================
-- aitest 데이터베이스 스키마 + 데이터
--
--   복원 : mysql -u test -p1234 aitest < util/db.sql
--   구성 : 1) 테이블 삭제  2) 테이블 생성  3) 데이터 입력
-- ==========================================================================

SET FOREIGN_KEY_CHECKS = 0;


-- ==========================================================================
-- 1. 테이블 삭제
-- ==========================================================================
DROP TABLE IF EXISTS `OrderItems`;
DROP TABLE IF EXISTS `OrderList`;
DROP TABLE IF EXISTS `Inventory`;
DROP TABLE IF EXISTS `Recipe`;
DROP TABLE IF EXISTS `Product`;
DROP TABLE IF EXISTS `Part`;
DROP TABLE IF EXISTS `User`;
DROP TABLE IF EXISTS `CODE`;


-- ==========================================================================
-- 2. 테이블 생성
-- ==========================================================================

-- CODE : 공통 코드 (AA/AU 권한, OS 주문상태, PS 상품상태)
CREATE TABLE `CODE` (
  `CODEID` varchar(100) NOT NULL,
  `CODE` varchar(100) DEFAULT NULL,
  `UPPER_CODE_ID` varchar(100) DEFAULT NULL,
  `CODE_NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CODEID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- User : 사용자 계정. CODEID 는 CODE.CODEID 참조
CREATE TABLE `User` (
  `IN_ID` varchar(100) NOT NULL,
  `ID` varchar(100) NOT NULL,
  `NAME` varchar(100) NOT NULL,
  `PASS` varchar(100) NOT NULL,
  `CODEID` varchar(100) NOT NULL,
  PRIMARY KEY (`IN_ID`),
  UNIQUE KEY `ID` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Part : 부품 마스터. STATE 는 CODE.CODEID(PS계열) 참조
CREATE TABLE `Part` (
  `PPID` varchar(100) NOT NULL,
  `NAME` varchar(100) DEFAULT NULL,
  `PRICE` varchar(100) DEFAULT NULL,
  `STATE` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`PPID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Product : 완제품 마스터. STATE 는 CODE.CODEID(PS계열) 참조
CREATE TABLE `Product` (
  `PID` varchar(100) NOT NULL,
  `NAME` varchar(100) NOT NULL,
  `PRICE` varchar(100) NOT NULL,
  `DES` varchar(100) DEFAULT NULL,
  `STATE` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`PID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Recipe : 완제품 구성 부품 (BOM). P_ID=Product.PID, PP_ID=Part.PPID
CREATE TABLE `Recipe` (
  `P_ID` varchar(100) NOT NULL,
  `PP_ID` varchar(100) NOT NULL,
  `COUNT` int(11) DEFAULT NULL,
  PRIMARY KEY (`P_ID`,`PP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Inventory : 재고. I_ID 는 Part.PPID 또는 Product.PID
CREATE TABLE `Inventory` (
  `seq` int(11) NOT NULL AUTO_INCREMENT,
  `I_ID` varchar(100) DEFAULT NULL,
  `QUANTITY` int(11) DEFAULT NULL,
  `DATE` datetime DEFAULT NULL,
  PRIMARY KEY (`seq`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- OrderList : 주문 헤더. STATE 는 CODE.CODEID(OS계열) 참조
CREATE TABLE `OrderList` (
  `U_ID` varchar(100) DEFAULT NULL,
  `STATE` varchar(100) DEFAULT NULL,
  `ORDER_DATE` datetime DEFAULT NULL,
  `COMP_DATE` datetime DEFAULT NULL,
  `ORDER_ID` varchar(100) NOT NULL,
  `ORDER_NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ORDER_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- OrderItems : 주문 상세. ORDER_ID=OrderList.ORDER_ID, P_ID=Product.PID
CREATE TABLE `OrderItems` (
  `ORDER_ID` varchar(100) NOT NULL,
  `P_ID` varchar(100) NOT NULL,
  `COUNT` int(11) DEFAULT NULL,
  PRIMARY KEY (`ORDER_ID`,`P_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


-- ==========================================================================
-- 3. 데이터 입력
-- ==========================================================================

-- CODE (20행)
INSERT INTO `CODE` (`CODEID`, `CODE`, `UPPER_CODE_ID`, `CODE_NAME`) VALUES
('AA001', 'AUTH_ADMIN', NULL, '시스템 관리자'),
('AU001', 'AUTH', NULL, '권한 관리'),
('AU002', 'AUTH_PARTNER', 'AU001', '업체 권한 그룹'),
('AU003', 'AUTH_USER', 'AU001', '사용자 권한 그룹'),
('AU004', 'AUTH_PARTNER_MASTER', 'AU002', '업체 마스터 관리자'),
('AU005', 'AUTH_PARTNER_MANAGER', 'AU002', '업체 일반 매니저'),
('AU006', 'AUTH_PARTNER_STAFF', 'AU002', '업체 직원'),
('AU007', 'AUTH_USER_VIP', 'AU003', 'VIP 일반 사용자'),
('AU008', 'AUTH_USER', 'AU003', '일반 회원'),
('OS001', 'ORD_STATE', NULL, '주문 상태 관리'),
('OS002', 'ORD_BEFORE_PROCESS', 'OS001', '제조 전 단계'),
('OS003', 'ORD_AFTER_PROCESS', 'OS001', '제조 및 완료 단계'),
('OS004', 'ORD_RECEIPT', 'OS002', '주문 접수'),
('OS005', 'ORD_PROCESS', 'OS003', '제조 중'),
('OS006', 'ORD_SHIPPING', 'OS003', '배송'),
('OS008', 'ORD_CANCLE', 'OS002', '주문 취소'),
('PS001', 'ITEM_STATE', NULL, '상품 상태 관리'),
('PS002', 'ITEM_ACTIVE', 'PS001', '활성'),
('PS003', 'ITEM_INACTIVE', 'PS001', '비활성'),
('PS004', 'ITEM_DELETE', 'PS001', '삭제');

-- User (4행)
INSERT INTO `User` (`IN_ID`, `ID`, `NAME`, `PASS`, `CODEID`) VALUES
('USR001', 'admin', '최관리', '1234', 'AA001'),
('USR002', 'manager', '홍길동', '1234', 'AU004'),
('USR003', 'staff', '김철수', '1234', 'AU006'),
('USR004', 'user', '이영희', '1234', 'AU008');

-- Part (12행)
INSERT INTO `Part` (`PPID`, `NAME`, `PRICE`, `STATE`) VALUES
('P001', '인텔 Core i5 CPU', '250000', NULL),
('P002', '인텔 Core i7 CPU', '420000', NULL),
('P003', 'AMD 라이젠 7 CPU', '380000', NULL),
('P004', 'DDR5 16GB RAM', '65000', NULL),
('P005', 'DDR5 32GB RAM', '130000', NULL),
('P006', 'NVMe SSD 1TB', '95000', NULL),
('P007', 'NVMe SSD 2TB', '180000', NULL),
('P008', 'RTX 4060 그래픽카드', '450000', NULL),
('P009', 'RTX 4070 Ti 그래픽카드', '980000', NULL),
('P010', '정격 700W 파워서플라이', '75000', NULL),
('P011', '정격 850W 파워서플라이', '120000', NULL),
('P012', '미들타워 PC 케이스', '60000', NULL);

-- Product (6행)
INSERT INTO `Product` (`PID`, `NAME`, `PRICE`, `DES`, `STATE`) VALUES
('PROD01', '사무용 가성비 PC', '654000', '문서 작업 및 웹서핑 전용 PC', 'PS002'),
('PROD02', '메인스트림 게이밍 PC', '1272000', '가성비 좋은 게이밍 컴퓨터', 'PS002'),
('PROD03', '하이엔드 게이밍 몬스터 PC', '2424000', '고사양 게임 및 영상 편집용 PC', 'PS002'),
('PROD04', 'AMD 원픽 게이밍 PC', '2118000', '원활한 멀티태스킹을 위한 AMD PC', 'PS002'),
('PROD05', '초고속 스토리지 워크스테이션', '1470000', '대용량 파일 작업 전용 컴퓨터', 'PS002'),
('PROD06', '컴팩트 미니 PC', '582000', '공간 활용도가 높은 미니 컴퓨터', 'PS004');

-- Recipe (32행)
INSERT INTO `Recipe` (`P_ID`, `PP_ID`, `COUNT`) VALUES
('PROD01', 'P001', 1),
('PROD01', 'P004', 1),
('PROD01', 'P006', 1),
('PROD01', 'P010', 1),
('PROD01', 'P012', 1),
('PROD02', 'P001', 1),
('PROD02', 'P004', 2),
('PROD02', 'P006', 1),
('PROD02', 'P008', 1),
('PROD02', 'P010', 1),
('PROD02', 'P012', 1),
('PROD03', 'P002', 1),
('PROD03', 'P005', 2),
('PROD03', 'P007', 1),
('PROD03', 'P009', 1),
('PROD03', 'P011', 1),
('PROD03', 'P012', 1),
('PROD04', 'P003', 1),
('PROD04', 'P005', 1),
('PROD04', 'P006', 1),
('PROD04', 'P009', 1),
('PROD04', 'P011', 1),
('PROD04', 'P012', 1),
('PROD05', 'P002', 1),
('PROD05', 'P005', 1),
('PROD05', 'P007', 3),
('PROD05', 'P010', 1),
('PROD05', 'P012', 1),
('PROD06', 'P001', 1),
('PROD06', 'P004', 1),
('PROD06', 'P006', 1),
('PROD06', 'P010', 1);

-- Inventory (18행)
INSERT INTO `Inventory` (`seq`, `I_ID`, `QUANTITY`, `DATE`) VALUES
(1, 'P001', 100, '2026-07-31 10:49:30'),
(2, 'P002', 35, '2026-07-31 10:49:30'),
(3, 'P003', 40, '2026-07-31 10:49:30'),
(4, 'P004', 108, '2026-07-31 10:49:30'),
(5, 'P005', 100, '2026-07-31 10:49:30'),
(6, 'P006', 38, '2026-07-31 10:49:30'),
(7, 'P007', 40, '2026-07-31 10:49:30'),
(8, 'P008', 25, '2026-07-31 10:49:30'),
(9, 'P009', 15, '2026-07-31 10:49:30'),
(10, 'P010', 18, '2026-07-31 10:49:30'),
(11, 'P011', 40, '2026-07-31 10:49:30'),
(12, 'P012', 28, '2026-07-31 10:49:30'),
(13, 'PROD01', 14, '2026-08-02 09:00:00'),
(14, 'PROD02', 14, '2026-08-02 09:00:00'),
(15, 'PROD03', 4, '2026-08-02 09:00:00'),
(16, 'PROD04', 6, '2026-08-02 09:00:00'),
(17, 'PROD05', 8, '2026-08-02 09:00:00'),
(18, 'PROD06', 18, '2026-08-02 09:00:00');

-- OrderList (21행)
INSERT INTO `OrderList` (`U_ID`, `STATE`, `ORDER_DATE`, `COMP_DATE`, `ORDER_ID`, `ORDER_NAME`) VALUES
('admin', 'OS008', '2026-08-01 08:14:48', NULL, 'admin20260801081448.545', '메인스트림 게이밍 PC 외 4건'),
('admin', 'OS008', '2026-08-01 08:53:17', NULL, 'admin20260801085317.365', '사무용 가성비 PC 외 2건'),
('admin', 'OS008', '2026-08-01 09:07:48', NULL, 'admin20260801090748.351', '컴팩트 미니 PC'),
('admin', 'OS004', '2026-08-01 09:45:08', NULL, 'admin20260801094508.907', 'AMD 원픽 게이밍 PC 외 2건'),
('admin', 'OS004', '2026-08-01 09:54:48', NULL, 'admin20260801095448.808', '사무용 가성비 PC 외 5건'),
('admin', NULL, '2026-08-01 10:40:03', NULL, 'admin20260801104003.330', '하이엔드 게이밍 몬스터 PC 외 2건'),
('admin', NULL, '2026-08-01 12:22:56', NULL, 'admin20260801122256.294', '메인스트림 게이밍 PC'),
('user', 'OS008', '2026-08-01 12:15:33', NULL, 'user20260801121533.852', '메인스트림 게이밍 PC 외 4건'),
('user', 'OS008', '2026-08-01 12:20:59', NULL, 'user20260801122059.930', '메인스트림 게이밍 PC 외 4건'),
('user', 'OS008', '2026-08-01 12:21:56', NULL, 'user20260801122156.156', '하이엔드 게이밍 몬스터 PC 외 3건'),
('user', 'OS008', '2026-08-01 12:21:59', NULL, 'user20260801122159.183', 'AMD 원픽 게이밍 PC'),
('user', 'OS008', '2026-08-01 12:22:10', NULL, 'user20260801122210.678', '하이엔드 게이밍 몬스터 PC'),
('user', 'OS004', '2026-08-01 12:27:50', NULL, 'user20260801122750.212', '초고속 스토리지 워크스테이션'),
('user', 'OS008', '2026-08-01 13:24:16', NULL, 'user20260801132416.011', '사무용 가성비 PC 외 5건'),
('user', 'OS006', '2026-08-01 13:33:33', NULL, 'user20260801133333.273', 'AMD 원픽 게이밍 PC'),
('user', 'OS008', '2026-08-01 13:33:39', NULL, 'user20260801133339.179', '하이엔드 게이밍 몬스터 PC'),
('user', 'OS004', '2026-08-01 13:33:46', NULL, 'user20260801133346.581', '사무용 가성비 PC'),
('user', 'OS004', '2026-08-01 13:33:51', NULL, 'user20260801133351.847', '컴팩트 미니 PC'),
('user', NULL, '2026-08-01 13:34:01', NULL, 'user20260801133401.196', '하이엔드 게이밍 몬스터 PC 외 5건'),
('user', NULL, '2026-08-01 13:34:13', NULL, 'user20260801133413.525', '하이엔드 게이밍 몬스터 PC 외 3건'),
('user', NULL, '2026-08-02 10:02:06', NULL, 'user20260802100206.620', '사무용 가성비 PC 외 4건');

-- OrderItems (124행)
INSERT INTO `OrderItems` (`ORDER_ID`, `P_ID`, `COUNT`) VALUES
('admin20260731233019.617', 'PROD03', 5),
('admin20260731233052.331', 'PROD01', 1),
('admin20260731233052.331', 'PROD02', 5),
('admin20260731233052.331', 'PROD03', 1),
('admin20260731233052.331', 'PROD04', 4),
('admin20260731233052.331', 'PROD05', 5),
('admin20260731233052.331', 'PROD06', 1),
('admin20260731234255.229', 'PROD01', 1),
('admin20260731234255.229', 'PROD02', 1),
('admin20260731234255.229', 'PROD03', 1),
('admin20260731234255.229', 'PROD04', 1),
('admin20260731234255.229', 'PROD05', 1),
('admin20260731234255.229', 'PROD06', 1),
('admin20260731234642.782', 'PROD01', 1),
('admin20260731234642.782', 'PROD02', 1),
('admin20260731234642.782', 'PROD03', 1),
('admin20260731234642.782', 'PROD04', 1),
('admin20260731234642.782', 'PROD05', 1),
('admin20260731234642.782', 'PROD06', 1),
('admin20260731234852.414', 'PROD01', 1),
('admin20260731234852.414', 'PROD02', 1),
('admin20260731234852.414', 'PROD03', 1),
('admin20260731234852.414', 'PROD04', 1),
('admin20260731234852.414', 'PROD05', 1),
('admin20260731235055.543', 'PROD01', 1),
('admin20260731235055.543', 'PROD02', 1),
('admin20260731235055.543', 'PROD03', 1),
('admin20260731235055.543', 'PROD04', 1),
('admin20260731235055.543', 'PROD05', 1),
('admin20260731235055.543', 'PROD06', 1),
('admin20260731235311.476', 'PROD01', 1),
('admin20260731235311.476', 'PROD02', 1),
('admin20260731235311.476', 'PROD03', 1),
('admin20260731235311.476', 'PROD04', 1),
('admin20260731235311.476', 'PROD05', 1),
('admin20260731235311.476', 'PROD06', 1),
('admin20260731235459.260', 'PROD01', 1),
('admin20260731235459.260', 'PROD02', 1),
('admin20260731235459.260', 'PROD03', 1),
('admin20260731235459.260', 'PROD04', 1),
('admin20260731235459.260', 'PROD05', 1),
('admin20260731235459.260', 'PROD06', 1),
('admin20260801002406.425', 'PROD03', 1),
('admin20260801002406.425', 'PROD04', 1),
('admin20260801002406.425', 'PROD05', 1),
('admin20260801002406.425', 'PROD06', 1),
('admin20260801010428.401', 'PROD02', 1),
('admin20260801010428.401', 'PROD03', 1),
('admin20260801010428.401', 'PROD05', 5),
('admin20260801010428.401', 'PROD06', 1),
('admin20260801013723.186', 'PROD03', 1),
('admin20260801013723.186', 'PROD04', 1),
('admin20260801013723.186', 'PROD05', 4),
('admin20260801013723.186', 'PROD06', 1),
('admin20260801045220.508', 'PROD01', 1),
('admin20260801045220.508', 'PROD02', 1),
('admin20260801045220.508', 'PROD03', 1),
('admin20260801045220.508', 'PROD04', 3),
('admin20260801045220.508', 'PROD05', 1),
('admin20260801045220.508', 'PROD06', 1),
('admin20260801081448.545', 'PROD02', 1),
('admin20260801081448.545', 'PROD03', 1),
('admin20260801081448.545', 'PROD04', 1),
('admin20260801081448.545', 'PROD05', 1),
('admin20260801081448.545', 'PROD06', 1),
('admin20260801085317.365', 'PROD01', 3),
('admin20260801085317.365', 'PROD02', 1),
('admin20260801085317.365', 'PROD04', 1),
('admin20260801090748.351', 'PROD06', 15),
('admin20260801094508.907', 'PROD04', 1),
('admin20260801094508.907', 'PROD05', 1),
('admin20260801094508.907', 'PROD06', 1),
('admin20260801095448.808', 'PROD01', 1),
('admin20260801095448.808', 'PROD02', 1),
('admin20260801095448.808', 'PROD03', 1),
('admin20260801095448.808', 'PROD04', 1),
('admin20260801095448.808', 'PROD05', 1),
('admin20260801095448.808', 'PROD06', 1),
('admin20260801104003.330', 'PROD02', 4),
('admin20260801104003.330', 'PROD03', 3),
('admin20260801104003.330', 'PROD04', 3),
('admin20260801122256.294', 'PROD02', 3),
('user20260801121533.852', 'PROD02', 1),
('user20260801121533.852', 'PROD03', 1),
('user20260801121533.852', 'PROD04', 1),
('user20260801121533.852', 'PROD05', 1),
('user20260801121533.852', 'PROD06', 1),
('user20260801122059.930', 'PROD02', 1),
('user20260801122059.930', 'PROD03', 2),
('user20260801122059.930', 'PROD04', 1),
('user20260801122059.930', 'PROD05', 2),
('user20260801122059.930', 'PROD06', 2),
('user20260801122156.156', 'PROD03', 1),
('user20260801122156.156', 'PROD04', 1),
('user20260801122156.156', 'PROD05', 1),
('user20260801122156.156', 'PROD06', 3),
('user20260801122159.183', 'PROD04', 1),
('user20260801122210.678', 'PROD03', 11),
('user20260801122750.212', 'PROD05', 6),
('user20260801132416.011', 'PROD01', 1),
('user20260801132416.011', 'PROD02', 1),
('user20260801132416.011', 'PROD03', 1),
('user20260801132416.011', 'PROD04', 1),
('user20260801132416.011', 'PROD05', 1),
('user20260801132416.011', 'PROD06', 1),
('user20260801133333.273', 'PROD04', 1),
('user20260801133339.179', 'PROD03', 5),
('user20260801133346.581', 'PROD01', 5),
('user20260801133351.847', 'PROD06', 5),
('user20260801133401.196', 'PROD01', 1),
('user20260801133401.196', 'PROD02', 1),
('user20260801133401.196', 'PROD03', 1),
('user20260801133401.196', 'PROD04', 1),
('user20260801133401.196', 'PROD05', 1),
('user20260801133401.196', 'PROD06', 1),
('user20260801133413.525', 'PROD03', 1),
('user20260801133413.525', 'PROD04', 1),
('user20260801133413.525', 'PROD05', 1),
('user20260801133413.525', 'PROD06', 1),
('user20260802100206.620', 'PROD01', 1000),
('user20260802100206.620', 'PROD02', 1),
('user20260802100206.620', 'PROD03', 1),
('user20260802100206.620', 'PROD04', 1),
('user20260802100206.620', 'PROD05', 1);


SET FOREIGN_KEY_CHECKS = 1;
