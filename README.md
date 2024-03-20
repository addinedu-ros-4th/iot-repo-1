# 아두이노 기반 지능형 농작물 환경 제어 시스템

![Screenshot from 2024-03-20 20-58-24](https://github.com/addinedu-ros-4th/iot-repo-1/assets/103230856/74961e69-b1f1-4d2d-b0ce-0e8872fa8631)

- **개발 기간** : 2024년 3월 7일(목) ~ 3월 12일(화)

- **개발 환경**

<img src="https://img.shields.io/badge/Ubuntu 22.04 -E95420?style=for-the-badge&logo=Ubuntu&logoColor=white"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=yellow"> <img src="https://img.shields.io/badge/Arduino-00878F?style=for-the-badge&logo=arduino&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=black"> <img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"> <img src="https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white"> <img src="https://img.shields.io/badge/visual studio code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white"> 
  
## :seedling: 소개
- 아두이노와 다양한 센서들을 활용하여 지능형 농작물 환경 제어 시스템을 구축하는 것을 목표로 합니다.
- 농작물의 생장 환경을 모니터링하고 제어할 수 있게 합니다.
- 

## :two_men_holding_hands: 팀원 및 역할

|역할|이름|업무|
|------|---|---|
|**팀장**|도준엽|기기 간 통신|
|팀원|유윤하|GUI 제작 및 통합|
|팀원|임수빈|하드웨어 제어|    
|팀원|조성호|DB 및 통합|

### 경험 - IOT 프로젝트를 통해 각자가 원하는 것을 경험 해 보자!  
* 아두이노와 다양한 센서 사용
* 하드웨어 제어 경험
* 데이터 처리 및 통신 경험
* 실시간 모니터링, 시각화
    
 각자의 요구 사항을 충족 시켜 줄 수 있는 프로젝트에 대한 고민
 그러던 중 찾게 된 스마트팜(지능형 농작물 환경 제어 시스템)  
 스마트 팜을 알아보니..  

> 센서 모듈: DHT 센서, 조도 센서, 토양 수분 센서 등을 활용
> 
> 액추에이터: 물 주입 펌프, 농작물 조명을 제어할 수 있는 LED, 통풍장치 등
>    
> 아두이노 마이크로컨트롤러: 센서 데이터를 수집하고 액추에이터를 제어하는 데 사용,아두이노 Uno, ESP32
> 
> 데이터 통신: 센서 데이터를 수집하고 외부로 전달하기 위해 Wi-Fi, 블루투스, LoRa 등의 통신 기술을 활용
> 
> 데이터 저장 및 분석: 수집된 데이터를 저장하고 분석하여 농작물의 상태를 모니터링하고 예측하는 데 필요한 시스템이 필요.
> 
> 사용자 인터페이스: 농부나 사용자가 시스템을 모니터링하고 제어할 수 있는 사용자 인터페이스가 필요
  
각자가 원하는 개발 경험을 가질 수 있을 것으로 예상.  

### 도전 - 짧은 개발 기간 안에 하고자 하는 것들을 모두 완성 시켜 보자!  
프로젝트 기한은 총 5일간의 짧은 시간..   
기간 내에 원하는 기능을 모두 개발 해내는 것을 목표로 도전.  

## 기능 리스트


|번호|기능|설명|
|------|---|---|
|1|센서 출력 값 조회|각 센서들을 통해 값을 입력 받음. <br><br> - 온, 습도 센서 : 온 습도 측정 <br> - 조도 센서 : 어두움 정도를 측정 <br> - 토양 습도센서 : 토양의 습한 정도를 측정 <br> - 초음파 센서 : 식물 성장의 정도를 측정|
|2|온도 조절 기능|기준 온도보다 높을 경우, 쿨러를 통한 온도 낮춤 <br><br> - 선풍기를 통해 대기 습도 낮춤 <br> - 환기구 개폐|
|3|대기 습도 조절 기능|적정 습도보다 높을 경우 <br><br> - 선풍기를 통해 대기 습도 낮춤 <br> - 환기구 개폐|    
|4|토양 수분 조절 기능|적정 습도보다 낮을 경우, 펌프를 통해 토양 수분 공급|
|5|광도 공급 기능|어두움 정도가 일정 수치 이상일 경우 LED 밝기 제어|
|6|식물 모니터링|카메라 1 : 식물의 성장을 모니터링 <br> 카메라 2 : 선풍기와 환기구와 같은 모터 모니터링|
|7|특정 이벤트 조회|센서를 통한 이상 값 이벤트 발생, 캡쳐기능 발생 기록들을 조회 가능|

## 소프트웨어 및 하드웨어 구성
### 하드웨어 구성도  
![image](https://github.com/addinedu-ros-4th/iot-repo-1/assets/55430286/581911ac-92f8-457c-8d14-abe5bf92e8a9)

### 소프트웨어 구성도
![image](https://github.com/addinedu-ros-4th/iot-repo-1/assets/55430286/d4bbb682-bf9b-4076-ade6-4699dfbc1c45)
  
### 제어 알고리즘
![image](https://github.com/addinedu-ros-4th/iot-repo-1/assets/55430286/0689dede-2664-4ffd-a70f-003cfaac44a8)
  
### 통신 시 JSON
![image](https://github.com/addinedu-ros-4th/iot-repo-1/assets/55430286/c92a7d90-807a-49f0-ade2-42684fba7988)
  
## 시연 영상

[![Video Label](http://img.youtube.com/vi/ScW8iWov_TY/0.jpg)](https://www.youtube.com/watch?v=ScW8iWov_TY&t=2s)

## 후속 보완점
1. IOT에 맞는 통신인 MFCC를 사용하여 통신 체계 구축.
2. 한번에 여러 데이터를 JSON으로 주고 받는 점에 대해 다시 한번 고찰 -> 더 좋은 방법은 없는가?
3. 하드웨어 및 제어 방식에 관한 고찰 필요 -> 전력 부족한 부분은 어떻게 해결? 모터 간 제어 순서를 어떻게?
4. 서버 구조를 도입하여 서버에서 데이터 처리 후 각 파트별로 제어할 필요 있음.
5. 멀티 쓰레드 사용 시, 쓰레드 간 시작 및 중지에 관한 대처 방안, 대안 필요.
