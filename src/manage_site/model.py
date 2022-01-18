"""
TODO: Doc
"""

import yaml
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Sequence


@dataclass
class Photo:
    identifier: str
    text: str

    def to_dict(self) -> Any:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: Any) -> "Photo":
        return cls(**obj)


@dataclass
class Row:
    photos: Sequence[Photo]

    def to_dict(self) -> Any:
        return {
            "photos": [photo.to_dict() for photo in self.photos],
        }

    @classmethod
    def from_dict(cls, obj: Any) -> "Row":
        photos = [Photo.from_dict(photo) for photo in obj["photos"]]
        return cls(photos=photos)


@dataclass
class Data:
    """
    TODO: Doc
    """

    rows: Sequence[Row]

    def to_dict(self) -> Any:
        return {
            "rows": [row.to_dict() for row in self.rows],
        }

    @classmethod
    def from_dict(cls, obj: Any) -> "Data":
        # NOTE: We iterate the rows in *reverse* order, since the newest
        #       rows will be *appended* to the list!
        rows = [Row.from_dict(row) for row in reversed(obj["rows"])]
        return cls(rows=rows)

    def save(self, path: Path) -> None:
        obj = self.to_dict()
        with open(path, "w") as f:
            yaml.dump(
                obj,
                f,
                indent=2,
                default_flow_style=False,
            )

    @classmethod
    def load(cls, path: Path) -> "Data":
        with open(path) as f:
            obj = yaml.safe_load(f)
        return cls.from_dict(obj)
