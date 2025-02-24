import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from cena.core import root_logger
from cena.db.database import db
from cena.db.db_setup import create_session
from cena.db.models.event import Event
from cena.schema.user import GroupInDB
from cena.services.backups.exports import auto_backup_job
from cena.services.scheduler.global_scheduler import scheduler
from cena.services.scheduler.scheduler_utils import Cron, cron_parser
from cena.utils.post_webhooks import post_webhooks

logger = root_logger.get_logger()

# TODO Fix Scheduler


@scheduler.scheduled_job(trigger="interval", minutes=1440)
def purge_events_database():
    """
    Ran daily. Purges all events after 100
    """
    logger.info("Purging Events in Database")
    expiration_days = 7
    limit = datetime.datetime.now() - datetime.timedelta(days=expiration_days)
    session = create_session()
    session.query(Event).filter(Event.time_stamp <= limit).delete()
    session.commit()
    session.close()
    logger.info("Events Purges")


@scheduler.scheduled_job(trigger="interval", minutes=30)
def update_webhook_schedule():
    """
    A scheduled background job that runs every 30 minutes to
    poll the database for changes and reschedule the webhook time
    """
    session = create_session()
    all_groups: list[GroupInDB] = db.groups.get_all(session)

    for group in all_groups:

        time = cron_parser(group.webhook_time)
        job = JOB_STORE.get(group.name)

        if not job:
            logger.error(f"No job found for group: {group.name}")
            logger.info(f"Creating scheduled task for {group.name}")
            JOB_STORE.update(add_group_to_schedule(scheduler, group))
            continue

        scheduler.reschedule_job(
            job.scheduled_task.id,
            trigger="cron",
            hour=time.hours,
            minute=time.minutes,
        )

    session.close()
    logger.info(scheduler.print_jobs())


class ScheduledFunction:
    def __init__(
        self,
        scheduler: BackgroundScheduler,
        function,
        cron: Cron,
        name: str,
        args: list = None,
    ) -> None:
        self.scheduled_task = scheduler.add_job(
            function,
            trigger="cron",
            name=name,
            hour=cron.hours,
            minute=cron.minutes,
            max_instances=1,
            replace_existing=True,
            args=args,
        )


def add_group_to_schedule(scheduler, group: GroupInDB):
    cron = cron_parser(group.webhook_time)

    return {
        group.name: ScheduledFunction(
            scheduler,
            post_webhooks,
            cron=cron,
            name=group.name,
            args=[group.id],
        )
    }


def init_webhook_schedule(scheduler, job_store: dict):
    session = create_session()
    all_groups: list[GroupInDB] = db.groups.get_all(session)

    for group in all_groups:
        job_store.update(add_group_to_schedule(scheduler, group))

    session.close()

    return job_store


logger.info("----INIT SCHEDULE OBJECT-----")

JOB_STORE = {
    "backup_job": ScheduledFunction(scheduler, auto_backup_job, Cron(hours=00, minutes=00), "backups"),
}

JOB_STORE = init_webhook_schedule(scheduler=scheduler, job_store=JOB_STORE)

logger.info(scheduler.print_jobs())
scheduler.start()
