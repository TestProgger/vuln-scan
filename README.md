# vuln-scan

Запуск сервера
```bash
source venv/bin/activate
python manage.py runserver 0.0.0.0:10200
```

Запуск фронта (Новая вкладка терминала)
```bash
cd frontend
nom run dev
```

Запуск планировщика (Новая вкладка терминала)
```bash
source venv/bin/activate
celery -A config worker -L debug
```


