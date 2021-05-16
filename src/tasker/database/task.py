"""A Task object within the Database"""
import datetime

from .day import Day


class Task:
    def __init__(self, name: str, usual_start: datetime.time, 
                 usual_end:datetime.time, recur: list[Day]=[]) -> None:
        self.name = name
        self.recur = recur
        self.usual_start = usual_start
        self.usual_end = usual_end

    def to_dict(self) -> dict:
        """This class as a dictionary for JSON encoding"""
        return {'name': self.name,
                'recur': self.recur,
                'usual_start': self.usual_start.isoformat,
                'usual_end': self.usual_end.isoformat}


    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        """This class from a dictionary for JSON encoding"""
        return cls(name=d['name'],
                   recur=[Day.from_string(r) for r in d['recur']],
                   usual_start=datetime.time.\
                               fromisoformat(d['usual_start']),
                   usual_end=datetime.time.\
                               fromisoformat(d['usual_end']))

    @property
    def length(self) -> datetime.timedelta:
        """The 'usual' timedelta between the start and end times"""
        return self.usual_end - self.usual_start
