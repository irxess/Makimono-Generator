import yaml
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

@dataclass
class Ingredient:
    id: int
    name: str
    amount: Union[float, int]
    unit: str = 'g'
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
    group: int = 0
    svg_x: int = 0
    svg_y: int = 0
    y: int = 0

def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

Type = enum('add', 'bake', 'bowl', 'cut', 'fry', 'km', 'mortar', 'oven', 'pipe', 'saucepan', 'shape')
Temperature = enum('freeze', 'cold', 'room', 'warm', 'hot')

@dataclass
class Step:
    id: int
    time: str
    step_type: Type
    temperature: int
    ingredients_used: List[Ingredient]
    refined_ingredients_used: List[RefinedIngredient]
    short: str = ""
    long: str = ""
    depends_on = []
    svg = StepSVG()

@dataclass
class IngredientsOverview:
    name: str
    # step?
    total_amount: Union[int, float]

@dataclass
class Recipe:
    name: str
    date_created: str
    date_updated: str
    steps: List[Step]
    ingredients: List[IngredientsOverview]
    description: str = ""
    source: str = ""
    image: str = ""


