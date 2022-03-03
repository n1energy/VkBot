import gino
from gino.api import Gino

from app.admin.models import *
from app.quiz.models import *
from sqlalchemy.engine.url import URL
from app.store.database.gino import db


@dataclass
class Database:
    db: Gino

    def __init__(self, app: "Application"):
        self.app = app
        self.db: Optional[Gino] = None

    async def connect(self, *_, **kw):
        self._engine = await gino.create_engine(
            URL(
                drivername="asyncpg",
                host=self.app.config.database.host,
                database=self.app.config.database.database,
                username=self.app.config.database.user,
                password=self.app.config.database.password,
                port=self.app.config.database.port,
            ),
            min_size=1,
            max_size=1,
        )
        self.db = db
        self.db.bind = self._engine
        self.app.logger.info('Database connected')

    async def disconnect(self, *_, **kw):
        pass
        # if self.db and self.db.is_bound():
        #     await self.db.pop_bind().close()


        # if self.db is not None: await self.db.pop_bind().close()
        # self.app.logger.info('Database disconnected')

        # if self.db:
        #     await self.db.pop_bind().close()
        #     self._engine = None
        #     self.db: Optional[Gino] = None
