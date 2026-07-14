import signal
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging
from app.database.session import SessionLocal
from app.services.pipeline import run_crawl_job, run_full_pipeline

logger = get_logger("api")


def crawl_task() -> None:
    db = SessionLocal()
    try:
        job = run_crawl_job(db)
        logger.info("Scheduled crawl finished status=%s message=%s", job.status, job.message)
    finally:
        db.close()


def pipeline_task() -> None:
    db = SessionLocal()
    try:
        job = run_full_pipeline(db)
        logger.info("Scheduled pipeline finished status=%s message=%s", job.status, job.message)
    finally:
        db.close()


def start_scheduler() -> None:
    settings = get_settings()
    setup_logging()

    if not settings.scheduler_enabled:
        logger.info("Scheduler disabled. Worker idle.")
        while True:
            time.sleep(3600)
        return

    scheduler = BlockingScheduler()
    scheduler.add_job(
        crawl_task,
        trigger=IntervalTrigger(minutes=settings.crawl_interval_minutes),
        id="crawl",
        replace_existing=True,
    )
    scheduler.add_job(
        pipeline_task,
        trigger=IntervalTrigger(minutes=settings.pipeline_interval_minutes),
        id="full_pipeline",
        replace_existing=True,
    )

    def shutdown(signum, frame):
        logger.info("Worker shutting down")
        scheduler.shutdown(wait=False)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logger.info(
        "Scheduler started crawl=%sm pipeline=%sm",
        settings.crawl_interval_minutes,
        settings.pipeline_interval_minutes,
    )
    scheduler.start()


if __name__ == "__main__":
    start_scheduler()
