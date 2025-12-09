from app import create_app
import os

# Создаём приложение через фабричную функцию
app = create_app()

if __name__ == "__main__":
    # Порт, который можно переопределить через переменные окружения
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")

    app.run(host=host, port=port)
