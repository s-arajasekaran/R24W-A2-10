from utils import get_logger
from crawler.frontier import Frontier
from crawler.worker import Worker

class Crawler(object):
    def __init__(self, config, restart, md, frontier_factory=Frontier, worker_factory=Worker):
        self.config = config
        self.logger = get_logger("CRAWLER")
        self.frontier = frontier_factory(config, restart)
        self.workers = list()
        self.worker_factory = worker_factory
        self.metaData = md

    def start_async(self):
        self.workers = [
            self.worker_factory(worker_id, self.config, self.frontier, md = self.metaData)
            for worker_id in range(self.config.threads_count)]
        for worker in self.workers:
            worker.start()

    def start(self):
        self.start_async()
        self.join()
        self.metaData = self.workers[0].metaData
        return self.metaData

    def join(self):
        for worker in self.workers:
            worker.join()
