from application import create_app
from settings import DevelopmentConfig, TestingConfig

app = create_app(TestingConfig)

if __name__ == "__main__":
    app.run()
