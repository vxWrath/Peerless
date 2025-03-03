from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, Optional
from uuid import uuid4

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, PrivateAttr

from .namespace import Namespace

if TYPE_CHECKING:
    from .database import Database


class DataModel(PydanticBaseModel, Mapping):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    def __getattribute__(self, key: str) -> Any:
        if (
            key in super().__getattribute__('__pydantic_fields__').keys()
            and key not in super().__getattribute__('__pydantic_fields_set__')
        ):
            raise ValueError(f"'{self.__class__.__name__}.{key}' is not currently available")
        
        return super().__getattribute__(key)
    
    def __setitem__(self, key: str, val: Any) -> None:
        setattr(self, key, val)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)
    
    def __len__(self) -> int:
        return len(self.model_dump())

class LeagueData(DataModel):
    id: int
    teams: Namespace[str, 'Team'] = Field(default_factory=Namespace)

    _db: 'Database' = PrivateAttr(init=False)

class Team(PydanticBaseModel):
    token: str = Field(default_factory=lambda : str(uuid4()))

    role_name: str
    role_id: Optional[int] = None
    emoji_id: Optional[int] = None

class PlayerData(DataModel):
    id: int
    blacklisted: bool = False
    leagues: Namespace[int, 'PlayerLeagueData'] = Field(default_factory=Namespace)

    _db: 'Database' = PrivateAttr(init=False)

    def __getattribute__(self, key: str) -> Any:
        return super(PydanticBaseModel, self).__getattribute__(key)
    
class PlayerLeagueData(DataModel):
    player_id: int
    league_id: int
    demands: int = 3

    _db: 'Database' = PrivateAttr(init=False)