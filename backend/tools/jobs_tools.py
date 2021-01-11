import os

class Job:
    def __init__(self, jobs_directory: str, logger):
        self.job_name = ""
        self.jobs_directory = jobs_directory
        # self.job_directory = os.path.join(self.jobs_directory, self.job_name)
        self.logger = logger

    def create(self):
        self.logger.info(f"Creating new job with name {self.job_name}")
        job_directory = os.path.join(self.jobs_directory, f"{self.job_name}.xml")
        # with open(self.job_directory, "w+") as job_file:

