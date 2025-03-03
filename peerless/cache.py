import json
import os
from typing import Any, Dict, Iterable, Optional, Set, Tuple, Type, Union

from redis.asyncio.client import PubSub, Redis

from .models import LeagueData, PlayerData, PlayerLeagueData


class Cache:
    def __init__(self) -> None:
        self.redis: Redis
        self.pubsub: PubSub

    @classmethod
    async def create(cls):
        self = cls()

        self.redis = Redis(
            host = os.getenv("REDISHOST", "localhost"), 
            password = os.getenv("REDISPASSWORD"), 
            decode_responses = True,
            health_check_interval = 60,
            retry_on_timeout = True,
        )
        await self.redis.initialize()
        #self.pubsub = self.redis.pubsub()

        return self
    
    async def close(self) -> None:
        if hasattr(self, 'pubsub'):
            await self.pubsub.unsubscribe()
            await self.pubsub.aclose()
            
        await self.redis.aclose()
    
    async def _listener(self):
        pass
    
    async def hash_set(self, model: Union[LeagueData, PlayerData, PlayerLeagueData], *, identifier: str, keys: Iterable[str]) -> None:
        necessary_keys = {'league_id', 'player_id'} if isinstance(model, PlayerLeagueData) else {'id'}
        necessary_keys.update(keys)

        name = f"{model.__class__.__name__}:{identifier}"
        dump = model.model_dump(mode="json", include=necessary_keys)

        await self.redis.hset(name, mapping={
            k: json.dumps(v)
            for k, v in dump.items()
        }) # type: ignore
        await self.redis.hexpire(name, 60 * 60, *necessary_keys)

    async def hash_get[T: Union[LeagueData, PlayerData, PlayerLeagueData]](self, model_cls: Type[T], *, identifier: str, keys: Iterable[str]) -> Tuple[Optional[T], Set[str]]:
        necessary_keys = {'league_id', 'player_id'} if issubclass(model_cls, PlayerLeagueData) else {'id'}
        necessary_keys.update(keys)

        name = f"{model_cls.__name__}:{identifier}"

        if not await self.redis.exists(name):
            return (None, necessary_keys)
        
        necessary_keys = list(necessary_keys)
        data = await self.redis.hmget(name, necessary_keys) # type: ignore

        mapping: Dict[str, Any] = {}
        unretrieved: Set[str] = set()

        for i, key in enumerate(necessary_keys):
            loaded = json.loads(data[i])

            if data[i] is not None:
                mapping[key] = loaded
            else:
                unretrieved.add(key)

        return (model_cls.model_validate(mapping, strict=True), unretrieved)