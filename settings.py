import os

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static') # пустая папка, сюда будет собирать статику collectstatic
 
STATIC_URL = '/static/' # URL для шаблонов
 
 
STATICFILES_DIRS = (
 
os.path.join(PROJECT_ROOT, 'assets'),
 
)