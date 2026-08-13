서버를 돌린 폴더에 data.머시기 json 파일 생성됨 동일 폴더임 index.html이 같이 있어야함 

조별과제 샘플 폴더 내에서 

python -m http.server 9900  웹서버 구동됨 

client.ino를 아두이노 ide에 코드 복사해서 돌리면 (wifi 연결된 상태에서 핀정보는 알아서 변경) 
아두이노에서 임의 데이터 json으로 송신 서버에서 수신 json 파일에 추가 index.html 이용하여 웹서버에서 실시간 확인 가능 (DB 귀찮...);