##### Required:
* python3.6
* django 2.1
##### Optional:
* virtual env

##### Installation process:
* Clone repository: **git clone https://github.com/adrianashymoniak/FinanceManager**
* Create virtual env:  run command in terminal **python -m venv myvenv**
* Activate virtual env (optional): 
    - For Linux: **source myvenv/bin/activate**
    - For Windows **myenv\Scripts\activate**
* run: **pip install -r requirements.txt** (for installing required libraries in your virtual env)
* Make sure your virtual environment is activated and requirements are installed    
* Run migration: **python manage.py migrate --settings=finance_manager_app.settings.base_settings**
* Run migration: **python manage.py createsuperuser --settings=finance_manager_app.settings.base_settings**
* Run server locally: **python manage.py runserver --settings=finance_manager_app.settings.base_settings**
* Open browser and go to  **http://127.0.0.1:8000/**