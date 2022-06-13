### 오늘의 점심
- 하루 삼시세끼, “오늘 점심 뭐 먹지?” 고민해 본 사람들이 고민하는 사람들을 위해 만들어 보는 웹 서비스

### Introduction
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


### 프로젝트 정보
Getting Started
1. Crawling (요기요 자동 크롤링) - 셀레니움으로 직접 홈페이지에 접근해서 뷰티풀스프로 데이터 가져와 저장하는 방식
python crawling.py 실행 시 자동으로 크롤링 진행되며 restaurant_OO.csv 파일 생성됨, OO 부분은 카테고리 부분(50개의 음식점 정보 저장됨)
카테고리 별로 각각 설정하여 진행 후csv 합쳐서 restaurant.csv로 저장

2. DB에 데이터 저장
python auto_publish.py 하여 migrations, migrate 진행 후 서버 자동실행 되므로 서버 종료 후
python auto_db_insert.py 하여 크롤링하여 가져온 restaurant.csv 데이터들 DB에 저장

Development Stack
📚 Frameworks, Platforms and Libraries
  ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
  ![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)
💾 Databases
  ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
🎈 Hosting/SaaS
  ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
💻 IDEs/Editors
  ![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
  ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
📋 Languages
  ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
  ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
  ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
🍗 ML/DL
  ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

✔ 컴파일 방법, 사용 환경, 브라우저 서포트, 개발스택, 구현 목록(명세)
✔ 간단한 사용 방법 및 예제
