from framework import Application
from middleware import fronts
from patterns.structural_patterns import AppRoute
import views


application = Application(AppRoute.routes, fronts)
application.run(port=8000)
