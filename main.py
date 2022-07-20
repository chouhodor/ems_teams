from project import create_app

app = create_app()
app.jinja_env.cache = {}