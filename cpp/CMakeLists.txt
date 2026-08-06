cmake_minimum_required(VERSION 3.28)

# 현재 폴더의 이름을 자동으로 추출해 실행 파일 이름으로 사용합니다.
get_filename_component(FOLDER_NAME "${CMAKE_CURRENT_SOURCE_DIR}" NAME)
project(${FOLDER_NAME} CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 👈 이제 정상적으로 동작합니다! 오직 이 폴더 직속에 있는 파일들만 수집합니다.
file(GLOB ALL_SOURCES
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cppm"
    "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp"
)

# 실행 파일 빌드 등록
add_executable(${FOLDER_NAME} ${ALL_SOURCES})

# 라이브러리 연동
target_link_libraries(${FOLDER_NAME} PRIVATE mariadb pthread)
