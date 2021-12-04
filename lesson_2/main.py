from create_db import create_db_if_not_exists
from framework import Application
from middleware import fronts
from patterns.structural_patterns import AppRoute
import views

# Создаем БД, если ее нет
create_db_if_not_exists()

application = Application(AppRoute.routes, fronts)
application.run(port=8000)
