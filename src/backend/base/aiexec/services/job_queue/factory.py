from aiexec.services.base import Service
from aiexec.services.factory import ServiceFactory
from aiexec.services.job_queue.service import JobQueueService


class JobQueueServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(JobQueueService)

    def create(self) -> Service:
        return JobQueueService()
