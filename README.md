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
│   └── ...    
│   
├── templates
│   ├── init/         // Init Page  
│   ├── users/        // Join, Login Page  
│   ├── main/         // Main Page  
│   ├── profile/      // Profile Page  
│   └── ...
│
└── manage.py // 메인
```