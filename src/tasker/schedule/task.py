"""A Task object within a Schedule"""
import datetime


class Task:
    def __init__(self, name: str, start: datetime.datetime, 
            end: datetime.datetime) -> None:
        self.name = name
        if end < start:
            raise ValueError(f"Task: {name} -- end ({end}) can not be "\
                             f"before start ({start}).")
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start_formatted}--{self.end_formatted}"\
                        f"-> {self.name}"

    @staticmethod
    def hour_minute_formatted(dt: datetime.datetime) -> str:
        return f"{dt.hour:02}:{dt.minute:02}"

    @property
    def start_formatted(self) -> str:
        return self.hour_minute_formatted(self.start)

    @property
    def end_formatted(self) -> str:
        return self.hour_minute_formatted(self.end)

    def to_dict(self) -> dict:
        """This class as a dictionary for JSON encoding"""
        return {'name': self.name,
                'end': self.end.isoformat(),
                'start': self.start.isoformat()}

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        """This class from a dictionary for JSON encoding"""
        return cls(name=d['name'],
                   start=datetime.time.fromisoformat(d['start']),
                   end=datetime.time.fromisoformat(d['end']))

    @classmethod
    def from_database_task(cls, database_task: "database.Task") -> "Task":
        return cls(name=database_task.name,
                   start=database_task.usual_start,
                   end=database_task.usual_end)

    def __lt__(self, other) -> bool:
        """Determine if this task starts before another task"""
        return self.start < other.start

    @property
    def length(self) -> datetime.timedelta:
        """The timedelta between the start and end times"""
        return self.end - self.start
