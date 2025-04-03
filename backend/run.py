import uvicorn
import subprocess


def migrate():
    subprocess.run(["alembic", "upgrade", "head"])


if __name__ == "__main__":
    migrate()
    uvicorn.run(
        "app.main:app", host="127.0.0.1", port=8000, reload=True
    )  # , debug=False)
