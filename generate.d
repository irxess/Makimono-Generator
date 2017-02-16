import yaml;
import std.stdio;
import diet.html;

struct Ingredient {
  string name;
  string amount;
  string unit;
}

enum Type { work, oven, fridge, freezer }

struct Step {
  int number;
  string description;
  string short_description;
  float time;
  Type type;
}

class Recipe {
  Ingredient[] ingredients;
  string name;
  string[] steps;
  // other properties
}

void main() {
  // for file in dir
  Recipe recipe = parse_recipe("recipe");

  // match ingredients against their yaml, find allergies

  // generate svg

  // create HTML using diet on template

}


Recipe parse_recipe(string filename) {
  Node recipe = Loader(filename ~ ".yaml").load();
  string name = recipe["recipe"].as!string;

  // create class

  Ingredient[] ingredients = [];
  foreach(Node n; recipe["ingredients"]) {
    Ingredient i = { name:n["name"].as!string, amount:n["amount"].as!string, unit:n["unit"].as!string };
    ingredients ~= i;
    writeln(n["name"].as!string);

    // read steps

  }

  Recipe recipe_class = new Recipe();
  recipe_class.ingredients = ingredients;
  recipe_class.name = name;

  // other properties

  return recipe_class;
}




