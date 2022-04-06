"""A Schedule as an object"""
import bisect
import datetime

from .task import Task


class ScheduleFailure(Exception):
    def __init__(self, tasks, next_task, error_msg):
        self._tasks = tasks
        self._next_task = next_task
        self._error_msg = error_msg

    def __str__(self):
        err_msg = "Successfully Added Tasks\n"
        err_msg += "\n".join(str(t) for t in self._tasks)
        err_msg += f"Next Task to Add:\n{self._next_task}\n"
        err_msg += f"Error Message:\n{self._error_msg}"
        return err_msg


class Schedule:
    def __init__(self, day_start: datetime.time, day_end: datetime.time,
            tasks: list[Task]=[]) -> None:
        self.day_start = day_start
        self.day_end = day_end
        self.tasks = []
        for t in tasks:
            self.add_task(t)

    def to_dict(self) -> dict:
        """This class as a dictionary for JSON encoding"""
        return {'day_start': self.day_start.isoformat(),
                'day_end': self.day_end.isoformat(),
                'tasks': [t.to_dict() for t in self.tasks]}

    @classmethod
    def from_dict(cls, d:dict) -> "Database":
        """This class from a dictionary for JSON encoding"""
        return cls(day_start=datetime.time.fromisoformat(d['day_start']),
                   day_end=datetime.time.fromisoformat(d['day_end']),
                   tasks=[Task.from_dict(t) for t in d['tasks']])

    def tasks_with_filled_gaps(self) -> list[Task]:
        """Return a list of Tasks with ??? Tasks in between specified tasks

        Returns
        -------
        list[Task]
            The tasks for the day, with ??? Tasks in between the specified
            tasks.
        """
        tasks = []

        try:
            if len(self.tasks) == 0:
                tasks.append(Task("???", start=self.day_start, 
                            end=self.day_end))
            else:
                # Add gap between day start and first task
                if self.tasks[0].start > self.day_start:
                    tasks.append(Task("???", start=self.day_start, 
                                end=self.tasks[0].start))
                # First (and only?) task
                tasks.append(self.tasks[0])

                # Remaining tasks
                if len(self.tasks) > 1:
                    for i, t in enumerate(self.tasks):
                        # Skip the first one, we already covered it
                        if i == 0:
                            continue
                        # Determine if there's a gap
                        previous_task = self.tasks[i-1]
                        if previous_task.end != t.start:
                            tasks.append(Task("???", start=previous_task.end, 
                                              end=t.start))
                        # This task
                        tasks.append(t)

                # Add gap between day end and last task
                if self.day_end > self.tasks[-1].end:
                    tasks.append(Task("???", start=self.tasks[-1].end,
                        end=self.day_end))

            return tasks
        except ValueError as exp:
            raise ScheduleFailure(tasks, t, str(exp))

    def __str__(self) -> str:
        return self.as_formatted_list_string()

    def as_latex_list(self, indent: int=0) -> str:
        """Return the schedule as a LaTeX list.

        Parameters
        ----------
        indent: int=0
            The number of tabs to indent the LaTeX list by.

        Returns
        -------
        str
            The schedule as a LaTeX list
        """
        list_str = "\t" * indent + "\\begin{itemize}\n"
        for t in self.tasks_with_filled_gaps():
            list_str += "\t" * indent
            list_str += f"\t\\item {t.start_formatted}--{t.end_formatted} "\
                        f"\\(\\rightarrow\\) "\
                        f"{t.name}\n"
        list_str += "\t" * indent + "\\end{itemize}"

        return list_str

    def as_formatted_list_string(self) -> str:
        """Return the schedule as a formatted list string.

        Returns
        -------
        str
            The schedule as a formatted list string.
        """
        task_strings = []

        task_id = 0
        for t in self.tasks_with_filled_gaps():
            if t.name == "???":
                task_strings.append(
                        f"  : {t}")
            else:
                task_strings.append(
                        f"{task_id:2}: {t}")
                task_id += 1

        return "\n".join(task_strings)

    def add_task(self, task: Task) -> None:
        bisect.insort(self.tasks, task)
