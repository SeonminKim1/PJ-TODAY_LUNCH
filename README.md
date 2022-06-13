![image](https://user-images.githubusercontent.com/87006912/173308040-4a80baf8-b228-47a6-a4e9-46b026fdc164.png)
## 오늘의 점심
- 하루 삼시세끼, “오늘 점심 뭐 먹지?” 고민해 본 사람들이 고민하는 사람들을 위해 만들어 보는 웹 서비스

## Introduction
- 주제 : 점심 추천 웹 서비스 (for 직딩, 일반인)
- 기간 : 2022.06.03 (금) ~ 2022.06.13 (월)

<hr>

### Structure
```
┌─today_lunch
│
├── today_lunch       // project
│   ├── urls.py       
│   ├── settings.py    
│   └── ...
│
├── users             // app
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── restaurant        // app
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── star              // app
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── static 
│   ├── css/          // css
│   ├── js/           // JS
│   └── img/          //images    
│   
├── templates
│   ├── init/         // Init Page  
│   ├── users/        // Join, Login Page  
│   ├── main/         // Main Page  
│   ├── profile/      // Profile Page  
│   └── ...
│
├── recommandation
│   ├── crawling.py      // Crawling
│   ├── db_uploader.py   // Restaurant data insert
│   ├── recommand.py     // User Based Recommandation
│   └── restaurant.csv   // restaurant data
│
├── manage.py // 메인
├── auto_db_insert.py
└── auto_publish.py
```

## Development Stack
#### 📚 Frameworks, Platforms and Libraries     
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)
#### 💾 Databases
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
#### 🎈 Hosting/SaaS
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
#### 💻 IDEs/Editors   
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
#### 📋 Languages    
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
#### 🍗 ML/DL    
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

## DB Modeling
![image](https://user-images.githubusercontent.com/87006912/173292061-a4710c4a-ad46-48bc-bdc6-a89acd377d4c.png)

## Figma mock up
![image](https://user-images.githubusercontent.com/87006912/173303730-37dea9f0-4aad-4fa4-ac9d-248fc19766e1.png)

## Gantt chart
https://docs.google.com/spreadsheets/d/1_1Sx46dnKnI8_DLJQzAASMSr7u525RFjm2Iat0beU14/edit#gid=1212318893

## API Blueprint (Notion)
https://www.notion.so/1b59a28804b9451d97d7b0145dc658f3?v=fb5a1b50406d43699b83a1d38aa2986c


## Getting Started
1. Crawling (요기요 자동 크롤링) - 셀레니움으로 직접 홈페이지에 접근해서 뷰티풀스프로 데이터 가져와 저장하는 방식
python crawling.py 실행 시 자동으로 크롤링 진행되며 restaurant_OO.csv 파일 생성됨, OO 부분은 카테고리 부분(50개의 음식점 정보 저장됨)
카테고리 별로 각각 설정하여 진행 후csv 합쳐서 restaurant.csv로 저장

2. DB에 데이터 저장
```python auto_publish.py``` 하여 migrations, migrate 진행 후 서버 자동실행 되므로 서버 종료 후    
```python auto_db_insert.py``` 하여 크롤링하여 가져온 restaurant.csv 데이터들 DB에 저장

3. sklearn 패키지 없을 경우 다운로드 필요
``` pip install sklearn ```

## Development
#### User Page
- 최초 페이지에서 회원가입, 로그인 페이지 이동
- 회원가입/로그인 기능
- 회원가입 vaildation
- 카카오지도API를 이용한 주소검색기능
#### Nav
- 홈버튼, 환영문구, 스코어링, 마이페이지, 로그아웃
#### Scoring Page
- 로그인 시 스코어링 페이지로 이동
- 아직 평점을 매기지 않은 음식점 중 랜덤 5개 출력
- 음식점 마다 별 1개 ~ 5개 선택해서 평점 부여
- '별점 저장하기' 클릭 시 평점 부여한 음식점들만 평점 등록됨
- '평가 그만하기' 클릭 시 메인 페이지로 이동
#### aside
- 사용자 정보(이름, 주소) 출력
- 오늘의 추천 - 어제 평점이 가장 높았던 음식점 중 랜덤 1개 추천
#### Main Page
- '사용자님과 가장 유사한 OOO님의 추천 음식점입니다!' 
    - 사용자기반 필터링을 이용한 나와 가장 비슷한 이용자의 top 5 음식점 출력
    - OOO님 클릭 시 유사도 팝오버 출력
- '점심 뭐 먹지? TOP 5' 
    - 카테고리 별 평균 평점이 가장 높은 음식점 TOP 5 (전체, 한식, 중식, 일식, 양식)
- 각 음식점들의 '상세보기'
    - 네이버 지도에 해당 음식점 검색 결과 출력
#### Mypage
- 점심일지 캘린더 형태로 출력
- 점심일지 등록
    - 빈 날짜 호버 시 '등록'버튼 출력
    - '등록'버튼 클릭 시 모달 창 출력
    - 음식점 선택(검색 가능)
    - 별점 선택
    - 등록 시 diary 데이터 insert, star 데이터 평점, 평가횟수 update
- 점심일지 수정/삭제
    - 등록된 점심일지 부분 클릭시 모달 창 출력
    - 별점 수정 시 diary 데이터, star 테이블 데이터 update
    - 삭제 클릭시 해당 점심일지 삭제됨
