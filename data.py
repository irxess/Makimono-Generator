import yaml
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

@dataclass
class Ingredient:
    #id: int
    name: str
    amount: Union[float, int]
    unit: str = ''
    comment: Optional[str] = None

@dataclass
class RefinedIngredient:
    name: str
    amount: Union[float, int, None] = None
    unit: Optional[str] = None

@dataclass
class StepTime:
    active: int = 0
    passive: int = 0

@dataclass
class StepSVG:
    x: int = 0
    y: int = 0
    svg_x: int = 0
    svg_y: int = 0
    group: int = 0

def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

Type = enum('add', 'bake', 'bowl', 'cut', 'fry', 'km', 'mortar', 'oven', 'pipe', 'saucepan', 'shape')
Temperature = enum('freeze', 'cold', 'room', 'warm', 'hot')

@dataclass
class Step:
    id: int
    time: StepTime
    step_type: Type
    temperature: Temperature
    ingredients_used: List[Ingredient]
    refined_ingredients_used: List[RefinedIngredient]
    depends_on: List[int]
    short: str = ""
    long: str = ""
    svg = StepSVG()

@dataclass
class IngredientsOverview:
    name: str
    # step?
    total_amount: Union[int, float]
    unit: str = ''
    comment: Optional[str] = None

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Line:
    start: Point
    end: Point
    color: Temperature

@dataclass
class Circle:
    color: Temperature
    center: Point
    step_type: Type

@dataclass
class Timeline:
    circles: List[Circle]
    lines: List[Line]
    height: int = 0

@dataclass
class Recipe:
    name: str
    date_created: str
    date_updated: str
    steps: List[Step]
    ingredients: List[IngredientsOverview]
    timeline: Timeline = Timeline([],[])
    description: str = ""
    source: str = ""
    image: str = ""


