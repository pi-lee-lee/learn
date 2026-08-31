#!/bin/bash

# ================= 설정 섹션 ================dsd
# 1. 원본 .ui 파일들이 있는 소스 디렉토리 경로
UI_SOURCE_DIR="/Users/idong-u/project/learn/과제/1/ui"

# 2. 변환된 .py 파일들을 저장할 대상 디렉토리 경로
PY_OUTPUT_DIR="/Users/idong-u/project/learn/과제/1/ui/py"
# ============================================

# 대상 디렉토리가 없으면 자동으로 생성
if [ ! -d "$PY_OUTPUT_DIR" ]; then
    mkdir -p "$PY_OUTPUT_DIR"
    echo -e "\033[36m[알림] 출력 디렉토리를 생성했습니다: $PY_OUTPUT_DIR\033[0m"
fi

# 소스 디렉토리에서 .ui 파일 목록 가져오기
# (shopt로 파일이 없을 때 빈 문자열로 처리되도록 설정)
shopt -s nullglob
uiFiles=("$UI_SOURCE_DIR"/*.ui)

if [ ${#uiFiles[@]} -eq 0 ]; then
    echo -e "\033[31m[오류] 변환할 .ui 파일이 소스 디렉토리에 없습니다.\033[0m"
    exit 1
fi

echo -e "\033[33m총 ${#uiFiles[@]}개의 UI 파일 변환을 시작합니다...\033[0m\n"

for uiPath in "${uiFiles[@]}"; do
    # 파일명 추출 (예: main.ui)
    fileName=$(basename "$uiPath")
    # 확장자 제외한 이름 추출 (예: main)
    baseName="${fileName%.*}"
    # 소문자로 변환 (기존 파워쉘 스크립트 동작 유지)
    baseNameLower=$(echo "$baseName" | tr '[:upper:]' '[:lower:]')
    
    pyFileName="${baseNameLower}.py"
    pyPath="${PY_OUTPUT_DIR}/${pyFileName}"

    # pyuic5 명령어 실행 (-x 옵션 유지)
    pyuic5 -x "$uiPath" -o "$pyPath"

    # 실행 결과 확인 ($?는 직전 명령어의 종료 상태 코드)
    if [ $? -eq 0 ]; then
        echo -e "\033[32m✔ 성공: $fileName ➔ $pyFileName\033[0m"
    else
        echo -e "\033[31m✘ 실패: $fileName 변환 중 오류 발생\033[0m"
    fi
done

echo -e "\n\033[36m🎉 모든 변환 작업이 완료되었습니다!\033[0m"
