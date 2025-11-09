from app import create_app
import schedule, time
from threading import Thread

app = create_app()

def auto_run():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    Thread(target=auto_run, daemon=True).start()
    app.run(debug=True)
