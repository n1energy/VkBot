from asyncio import Task
import asyncio
from typing import Optional

from app.store import Store


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        self.poll_task = asyncio.create_task(self.poll())
        self.poll_task.add_done_callback
        self.is_running=True

    async def stop(self):
        self.is_running = False
        await self.poll_task

    async def poll(self):
        while self.is_running:
            await self.store.vk_api.poll()
