"""An enum representing days of the week"""
from enum import Enum, unique

@unique
class Day(Enum):
   # Starts with Monday as 0 to match datetime format for weekday.
   MONDAY=0
   TUESDAY=1
   WEDNESDAY=2
   THURSDAY=3
   FRIDAY=4
   SATURDAY=5
   SUNDAY=6
   DAILY=7

   def to_string(self) -> str:
       """This class as a string for JSON encoding"""
       return self.name

   @classmethod
   def from_string(cls, name:str) -> "Day":
       """This class from a from for JSON encoding"""
       return cls[name.upper()]
