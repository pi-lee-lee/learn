# ?? [오류 해결] 파워셸 콘솔 출력을 UTF-8로 안전하게 지정
$OutputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

# ================= 경로 설정 =================
# 1. 원본 .ui 파일들이 모여있는 폴더 경로
$UI_SOURCE_DIR = "D:\python\learn\과제\1\ui"

# 2. 변환된 .py 파일들을 저장할 출력 폴더 경로
$PY_OUTPUT_DIR = "D:\python\learn\과제\1\ui\py"
# ============================================

# 출력 폴더가 없으면 자동으로 생성
if (-not (Test-Path $PY_OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $PY_OUTPUT_DIR | Out-Null
    Write-Host "[알림] 출력 폴더를 생성했습니다: $PY_OUTPUT_DIR" -ForegroundColor Cyan
}

# 원본 폴더에서 .ui 파일 목록 가져오기
$uiFiles = Get-ChildItem -Path $UI_SOURCE_DIR -Filter "*.ui"

if ($uiFiles.Count -eq 0) {
    Write-Host "? 변환할 .ui 파일이 소스 폴더에 없습니다." -ForegroundColor Red
    Exit
}

Write-Host "총 $($uiFiles.Count)개의 UI 파일 변환을 시작합니다...`n" -ForegroundColor Yellow

foreach ($file in $uiFiles) {
    $uiPath = $file.FullName
    $baseName = $file.BaseName.ToLower()
    $pyFileName = "$baseName.py"
    $pyPath = Join-Path $PY_OUTPUT_DIR $pyFileName

    # pyuic5 명령어 실행 (-x 옵션 포함)
    & pyuic5 -x "$uiPath" -o "$pyPath"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "? 성공: $($file.Name) ?? $pyFileName" -ForegroundColor Green
    } else {
        Write-Host "? 실패: $($file.Name) 변환 중 에러 발생" -ForegroundColor Red
    }
}

Write-Host "`n?? 모든 변환 작업이 완료되었습니다!" -ForegroundColor Cyan
