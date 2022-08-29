![image](https://user-images.githubusercontent.com/87006912/173308040-4a80baf8-b228-47a6-a4e9-46b026fdc164.png)
## 👉 오늘의 점심
- 하루 삼시세끼, “오늘 점심 뭐 먹지?” 고민해 본 사람들이 고민하는 사람들을 위해 만들어 보는 웹 서비스

## 👉 Introduction
- **주제** : 점심 추천 웹 서비스 (for 직딩, 일반인)
- **기간** : 2022.06.03 (금) ~ 2022.06.13 (월)
- **Team** : 김선민 ([Github](https://github.com/SeonminKim1)), 김민기 ([Github](https://github.com/kmingky)), 박재현 ([Github](https://github.com/Aeius)), 황신혜 ([Github](https://github.com/hwangshinhye)) 

<hr>

## 👉 Project-Rules
#### Schedule Management : [Git Project Link](https://github.com/SeonminKim1/TODAY_LUNCH/projects/1), [간트차트 Link](https://docs.google.com/spreadsheets/d/1_1Sx46dnKnI8_DLJQzAASMSr7u525RFjm2Iat0beU14/edit#gid=1212318893)
#### API Design : [Notion-link](https://www.notion.so/1b59a28804b9451d97d7b0145dc658f3?v=fb5a1b50406d43699b83a1d38aa2986c)
#### Branch Info
- main : LocalHost 실행 branch
- publish : EC2 Hosting 실행 Branch

#### Figma Mock-up
![image](https://user-images.githubusercontent.com/87006912/173303730-37dea9f0-4aad-4fa4-ac9d-248fc19766e1.png)

#### DB Modeling   
![image](https://user-images.githubusercontent.com/33525798/173334447-cbf70e34-82a3-47af-844a-0c6e4804c394.png)

<hr>

## 👉 Development-Stack
#### 📚 Frameworks, Libraries (ML) 
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) 

#### 💾 Databases, Hosting/Storage
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)      

#### 📋 Languages
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)    

#### 💻 IDEs/Editors
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)    

<hr>

## 👉 Getting-Started

``` Run
$ pip install -r requirements.txt
$ python recommandtion/crawling.py  # Crawing Data
$ python auto_publish.py            # Data Migrations & Run Server
$ python auto_db_insert.py          # Insert Restaurant DB 

# publish branch version 
$ sh auto_delete_db.sh
$ sh auto_publish.sh
```

#### Crawling 
- 요기요 홈페이지 카테고리별 음식점 데이터 크롤링 (python crawling.py)
- 생성된 restaurant_OO.csv 파일 (OO 부분은 카테고리, 50개의 음식점 정보 저장)들 합쳐서 최종 restaurant.csv 생성

#### DB Migration & DB 
- (main Branch) ```python auto_publish.py``` 하여 migrations, migrate 진행
- (main Branch) ```python auto_db_insert.py``` 하여 크롤링 데이터(restaurant.csv)들 DB에 저장
- (publish branch) ```sh auto_delete_db.sh``` 하여 migrations, sqlite3 db 초기화
- (publish branch) ```sh auto_publish.sh``` 하여 DB Migrations 및 크롤링 데이터(restaurant.csv) DB 저장

<hr>

## 👉 Structure
```
┌─today_lunch
├── today_lunch         // project
│   ├── urls.py       
│   ├── settings.py     // setting
│   └── ...
├── users               // app
│   ├── models.py       // DB Model - User
│   ├── views.py
│   └── ...
├── restaurant          // app
│   ├── models.py       // DB Model - Restaurant, Category
│   ├── views.py
│   └── ...
├── star                // app
│   ├── models.py       // DB Model - Star 
│   ├── views.py
│   └── ...
├── mypage              // app
│   ├── models.py       // DB Model - Diary
│   ├── views.py
│   └── ...
├── recommandation
│   ├── crawling.py     // Crawling
│   ├── db_uploader.py  // Restaurant data insert
│   ├── recommand.py    // User Based Recommandation
│   └── restaurant.csv  // restaurant data
├── static 
│   ├── css/            // css
│   └── img/            // images    
├── templates
│   ├── init/           // Init Page  
│   ├── users/          // Join, Login Page  
│   ├── main/           // Main Page  
│   ├── mypage/         // Profile Page  
│   └── ...
│
├── db.sqlite3          // DB  
├── manage.py           // 메인
├── auto_db_insert.py   
└── auto_publish.py
```

<hr>


## 👉 Development

#### User Page
- 시작 페이지 회원가입, 로그인 페이지 이동
- 회원가입/로그인 기능
- 회원가입 vaildation
- 카카오지도 API를 이용한 주소 검색 기능

#### Nav Bar
- 페이지 이동(홈, 평점페이지, 마이페이지, 로그아웃)

#### Scoring Page
- **로그인 후 스코어링 페이지 이동**
- **로그인 User 평점 이력 없는 음식점 5개 출력**
- **음식점 마다 별 1개 ~ 5개 선택해서 평점 부여 및 저장**
  - '별점 저장하기' 클릭 시 평점 부여한 음식점들만 평점 등록됨
  - '평가 그만하기' 클릭 시 메인 페이지로 이동

#### Aside (Main Page, MyPage)
- **사용자 정보(이름, 주소) 출력**
- **추천 컨텐츠 1) 오늘의 추천**
  - 어제 평점이 가장 높았던 음식점 1개 추천

#### Main Page
- **추천 컨텐츠 2) '사용자님과 가장 유사한 OOO님의 추천 음식점입니다!'**
  - User-Baed Filtering을 이용한 나와 가장 비슷한 유저의 top 5 음식점 출력
  - OOO님 클릭 시 유사도 팝오버 출력
- **추천 컨텐츠 3) '점심 뭐 먹지? TOP 5'**
  - 카테고리별 평균 평점이 가장 높은 음식점 TOP 5 (전체, 한식, 중식, 일식, 양식)
- **각 음식점들의 '상세보기'**
  - 네이버 지도에 해당 음식점 검색 결과 출력

#### Mypage
- **점심일지 캘린더 형태 출력**
- **점심일지 등록**
  - 빈 날짜 호버 시 '등록'버튼 출력, 클릭시 모달 출력
- **점심일지 등록 모달**
  - 음식점 선택 (+ 검색 가능) 
  - 별점 선택 (1 ~ 5)
  - 등록 내용 바탕으로 DB Update 및 추천 알고리즘 Upgrade
- **점심일지 수정/삭제**
  - 등록된 점심일지 부분 클릭시 모달 창 출력
  - 수정/삭제 내용 바탕으로 DB Update 및 추천 알고리즘 Upgrade
  - 삭제 클릭시 해당 점심일지 삭제됨

#### Publish and Storage Mount
- AWS EC2 이용한 외부 Publish 배포
- S3에 정적 이미지 파일들 관리 및 EC2에 Mount하여 구현

<hr>

## 👉 시연 화면
#### 첫화면, 회원가입, 로그인 화면
![image](https://user-images.githubusercontent.com/33525798/173514356-84840d07-2425-4095-b9fa-07d50a19bc0d.png)

#### 평가 페이지, 메인 페이지
![image](https://user-images.githubusercontent.com/33525798/173514477-228b4897-bee0-491e-847c-5720d11a5eb4.png)

#### 마이페이지 (점심일지 등록, 수정, 삭제)
![image](https://user-images.githubusercontent.com/33525798/173514527-8e456009-0dcb-4e5d-890a-e476ef4331fb.png)


## 🛡 Trouble Shooting
#### ⚡ 문제 발생
추천시스템이 작동하는 main 페이지 최초 접속 시 접속이 매우 느린상황 발생 (이후 이동은 캐시가 저장되어 빠르나, 새로운 회원, 캐시 없어진 경우 접속느림)

#### ⚡ 문제 원인
DB의 Star테아블의 데이터를 DataFrame으로 만들어서 이를 통한 추천을 해주는 과정에서 DB의 데이터가 쌓이면 쌓일수록 DataFrame을 생성하는 속도가 느려지는 것으로 확인

#### ⚡ 문제 해결
1. Recommend 클래스를 정의하여 DataFrame을 init하는 함수와 실제 유사도를 계산하는 부분들을 나눠서 각각 함수화하여 main접속 시 유사도만 계산될 수 있도록하여 속도 개선
2. 싱글톤 패턴을 이용하여 유사도 계산 시 하나의 인스턴스만 사용하여 리소스를 절약하도록하고 서버가 실행될 때 미리 해당 인스턴스를 생성하도록 __init__.py에서 클래스선언
3. 해당 인스턴스를 현재 DB에 맞게 실시간으로 갱신 시켜주기 위해 Thread를 이용하여 10초마다 __init__()함수 실행되도록 설정

#### ⚡ 해결 결과

##### 해결 전    
![image](https://user-images.githubusercontent.com/87006912/187224620-f64f8a47-963f-4a53-ad51-1382eefe0ef3.png)    
##### 해결 후    
![image](https://user-images.githubusercontent.com/87006912/187224651-eeafdfd5-9fed-41d2-a671-91bac8687caf.png)    

최초 서버가 실행될 때 이전보다 많은 시간이 소요되긴 하지만 클라이언트 입장으로써 접속지연같은 불편함을 개선할 수 있었다.
10초마다 갱신도 자연스럽게 되면서 서비스를 이용함에 있어서 접속 지연을 개선할 수 있었다.

블로그 정리 : https://psb6604.tistory.com/48?category=1059497
