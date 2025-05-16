import grpc.aio
# noinspection PyUnresolvedReferences
from .generated.task_worker_pb2 import GeoPoint, TaskRequest, TaskType
from .generated.task_worker_pb2_grpc import TaskWorkerStub
from models.models import CellTower


class TaskWorkerClient:
    _instance = None

    def __init__(self):
        self.channel = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Lazy initialization (create channel only when first used)
            cls._instance.channel = None
        return cls._instance

    async def get_stub(self):
        """Get or create the async stub (lazy initialization)"""
        if self.channel is None or await self.channel.channel_ready() is False:
            self.channel = grpc.aio.insecure_channel('task_worker:50051')
        return TaskWorkerStub(self.channel)

    async def process_task(self, towers: list[CellTower], task_type: TaskType):
        grpc_stub = await self.get_stub()

        points = [GeoPoint(lat=tower.lat, lng=tower.lon) for tower in towers]

        request = TaskRequest( points=points, task_type=task_type)
        return await grpc_stub.Process(request)


task_worker_client = TaskWorkerClient()
