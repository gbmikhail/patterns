from framework import Application
from middleware import fronts
from urls import routes

application = Application(routes, fronts)
application.run()
