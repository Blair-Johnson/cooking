from typing import List, Dict, Tuple, Union
from enum import Enum


class UnitType(Enum):
    TIME = "time"
    WEIGHT = "weight"
    VOLUME = "volume"
    TEMPERATURE = "temperature"

class UnitValue:
    CONVERT_TO_SI = {
            UnitType.TIME: {"seconds": lambda t: t, 
                            "minutes": lambda t: t*60, 
                            "hours": lambda t: t*3600},
            UnitType.WEIGHT: {"grams": lambda m: m, 
                              "kilograms": lambda m: m*1000, 
                              "pounds": lambda m: m*453.592},
            UnitType.VOLUME: {"milliliters": lambda v: v, 
                              "liters": lambda v: v*1000, 
                              "cups": lambda v: v*240, 
                              "ounces": lambda v: v*29.5735,
                              "tablespoons": lambda v: v*14.7868,
                              "teaspoons": lambda v: v*4.9289},
            UnitType.TEMPERATURE: {"celsius": lambda t: t,
                                   "fahrenheit": lambda t: (t-32)*5/9}
    }
    CONVERT_FROM_SI = {
            UnitType.TIME: {"seconds": lambda t: t, 
                            "minutes": lambda t: t/60, 
                            "hours": lambda t: t/3600},
            UnitType.WEIGHT: {"grams": lambda m: m, 
                              "kilograms": lambda m: m/1000, 
                              "pounds": lambda m: m/453.592},
            UnitType.VOLUME: {"milliliters": lambda v: v, 
                              "liters": lambda v: v/1000, 
                              "cups": lambda v: v/240, 
                              "ounces": lambda v: v/29.5735,
                              "tablespoons": lambda v: v/14.7868,
                              "teaspoons": lambda v: v/4.9289},
            UnitType.TEMPERATURE: {"celsius": lambda t: t,
                                   "fahrenheit": lambda t: (t*9/5)+32}
    }
    CONSUMABLE = {UnitType.WEIGHT, UnitType.VOLUME}

    def __init__(self, value: float, unit: str, unit_type: UnitType):
        if unit not in self.CONVERT_TO_SI[unit_type]:
            raise ValueError(f"Invalid unit '{unit}' for unit type {unit_type.value}")
        self.value = value
        self.unit = unit
        self.unit_type = unit_type

    def to_si(self) -> float:
        """Convert to SI units."""
        conversion = self.CONVERT_TO_SI[self.unit_type][self.unit]
        return conversion(self.value)

    def convert_to(self, target_unit: str) -> "UnitValue":
        """Convert to a target unit."""
        if target_unit not in self.CONVERT_TO_SI[self.unit_type]:
            raise ValueError(f"Invalid target unit '{target_unit}' for unit type {self.unit_type.value}")
        si_value = self.to_si()
        conversion = self.CONVERT_FROM_SI[self.unit_type][target_unit]
        return UnitValue(conversion(si_value), target_unit, self.unit_type)

    def __repr__(self):
        return f"{self.value} {self.unit}"
