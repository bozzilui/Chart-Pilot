from website import create_app
from website.dashapp import layout
import Plot_ichimoku

apps = create_app()

app = create_app()[0]
dashapp = create_app()[1]