import yaml
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field

@dataclass
class Ingredient:
    name: str
    amount: Union[float, int]
    unit: str = ''
    comment: Optional[str] = None
    recipe_link: Optional[str] = None

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
    group: int = 0 # One group per leaf node, parent belongs to group of child with smallest y-value used.

def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

Type = enum('add', 'bake', 'bowl', 'cut', 'fry', 'km', 'mortar', 'oven', 'pipe', 'saucepan', 'shape')
Temperature = enum('freeze', 'cold', 'room', 'warm', 'hot')

@dataclass
class Step:
    id: int
    step_type: Type
    temperature: Temperature
    time: StepTime = field(default_factory=lambda: StepTime())
    ingredients_used: List[Ingredient] = field(default_factory=lambda: [])
    refined_ingredients_used: List[RefinedIngredient] = field(default_factory=lambda: [])
    depends_on: List[int] = field(default_factory=lambda: [])
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
    recipe_link: Optional[str] = None

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
    height: int = 0
    circles: List[Circle] = field(default_factory=lambda: [])
    lines: List[Line] = field(default_factory=lambda: [])

@dataclass
class Source:
    name: str
    originality: Optional[str] = 'source' # source, adapted, inspired
    author: Optional[str] = None
    publication: Optional[str] = None
    url: Optional[str] = None
    date: Optional[str] = None

@dataclass
class Yield:
    amount: Union[int, float]
    unit: str
    qualification: Optional[str] = None

# @dataclass
# class ResultingAmounts:
#     yields: List[Yield] = field(default_factory=lambda: [])

@dataclass
class RecipeTime:
    lower_bound: int = 0
    upper_bound: int = 0

@dataclass
class Recipe:
    name: str
    not_ready_for_publish: Optional[bool] = field(init=False)
    date_created: str
    date_updated: str
    steps: List[Step] = field(default_factory=lambda: [])
    ingredients: List[IngredientsOverview] = field(default_factory=lambda: [])
    timeline: Timeline = field(default_factory=lambda: Timeline())
    # field(default_factory=lambda: StepTime(active = 0, passive = 0))
    description: str = ""
    source: Optional[Source] = None
    image: str = ""
    yields: List[Yield] = field(default_factory=lambda: [])
    url_name: str = ""
    time: RecipeTime = field(default_factory=lambda: RecipeTime())
