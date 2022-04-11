from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from cena.core.config import app_dirs, settings

app_dirs.DATA_DIR.joinpath("scheduler.db").unlink(missing_ok=True)
scheduler = BackgroundScheduler(jobstores={"default": SQLAlchemyJobStore(settings.SCHEDULER_DATABASE)})
