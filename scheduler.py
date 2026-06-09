import schedule
import time
import subprocess
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def run_pipeline():
    logging.info(f"Scheduler triggered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    result = subprocess.run(
        ["python3", "/home/muthukarthik/clouddrive/de-journey/day02.py"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        logging.info("Pipeline completed successfully")
    else:
        logging.error(f"Pipeline failed: {result.stderr}")

# Schedule every hour
# For testing we'll run every 2 minutes first
schedule.every(2).minutes.do(run_pipeline)

logging.info("Scheduler started - pipeline runs every 2 minutes")
logging.info("Press Ctrl+C to stop")

# Run immediately once first
run_pipeline()

# Then keep running on schedule
while True:
    schedule.run_pending()
    time.sleep(30)