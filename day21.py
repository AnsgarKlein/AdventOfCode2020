#!/usr/bin/env python3

from typing import List
from typing import Tuple
from typing import Union

import re

class Ingredient:
    def __init__(self, name: str, possible_allergens: List[str]):
        self.name = name
        self.possible_allergens = possible_allergens

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return self.name

    def __str__(self):
        if len(self.possible_allergens) == 0:
            return self.name
        else:
            return '{} (Maybe: {})'.format(self.name, ', '.join(self.possible_allergens))

    def add_possible_allergens(self, new_allergens: Union[str, List[str]]):
        if isinstance(new_allergens, str):
            self.add_possible_allergens([ new_allergens ])
            return

        for new_allergen in new_allergens:
            if new_allergen not in self.possible_allergens:
                self.possible_allergens.append(new_allergen)

class Food:
    def __init__(self, ingredients: List[Ingredient], definite_allergens: List[str]):
        self.ingredients = ingredients
        self.definite_allergens = definite_allergens

    def __str__(self):
        ingredient_names = ', '.join([ ingr.name for ingr in self.ingredients ])
        allergen_names = ', '.join(self.definite_allergens)
        return '{} (Definitely: {})'.format(ingredient_names, allergen_names)

def read_input_file(filename) -> Tuple[List[Ingredient], List[Food]]:
    all_ingredients: List[Ingredient] = []
    all_foods: List[Food] = []

    with open(filename, 'r') as input_file:
        content = input_file.read().split('\n')

        for line in content:
            if line.strip() == '':
                continue

            # Extract possible allergens in food
            allergens_match = re.match('.*(\(.*\))$', line)
            assert allergens_match is not None
            allergens = allergens_match.group(1)[10:-1].split(', ')

            # Extract ingredients
            ingredients_match = re.match('(.*) \(.*', line)
            assert ingredients_match is not None
            ingredients = ingredients_match.group(1).strip().split(' ')

            # Create Ingredients
            food_ingredients: List[Ingredient] = []
            for ingr_name in ingredients:
                ingr = None

                # Check if ingredient already exists and create it if not
                for ingr_check in all_ingredients:
                    if ingr_check.name == ingr_name:
                        ingr = ingr_check
                if ingr is None:
                    ingr = Ingredient(ingr_name, [])
                    all_ingredients.append(ingr)

                # Add possible allergens to ingredient
                ingr.add_possible_allergens(allergens)
                food_ingredients.append(ingr)

            # Create food
            food = Food(food_ingredients, allergens)
            all_foods.append(food)

    return all_ingredients, all_foods

def main():
    # Read input file
    all_ingredients, all_foods = read_input_file('day21_input.txt')

    # Create list of all allergens
    all_allergens = []
    for food in all_foods:
        for food_allergen in food.definite_allergens:
            if food_allergen not in all_allergens:
                all_allergens.append(food_allergen)
    all_allergens.reverse()

    #for ingr in all_ingredients:
    #    print('Ingredient: {}'.format(ingr))
    #for food in all_foods:
    #    print('Food: {}'.format(food))
    #for allergen in all_allergens:
    #    print('Allergen: {}'.format(allergen))
    #print()


    ############ PART ONE ############

    # Go through all allergens
    changed_something = True
    while changed_something == True:
        changed_something = False

        for allergen in all_allergens:
            # Get all foods that contain this allergen
            affected_foods = []
            for food in all_foods:
                if allergen in food.definite_allergens:
                    affected_foods.append(food)

            # Get all ingredients that might be responsible for this allergen
            possible_ingredients = []
            for food in affected_foods:
                for ingredient in food.ingredients:
                    if ingredient not in possible_ingredients:
                        possible_ingredients.append(ingredient)

            # Search the ingredient responsible for the allergen
            responsible_ingredient = None

            # If there is a food that has only one ingredient this
            # ingredient must be responsible for the allergen
            for food in affected_foods:
                if len(food.ingredients) == 1:
                    responsible_ingredient = food.ingredients[0]

            # Check which ingredient is present in every food
            if responsible_ingredient is None:
                responsible_ingredients = []
                for ingredient in possible_ingredients:
                    contained_in_all_foods = True
                    for food in affected_foods:
                        if ingredient not in food.ingredients:
                            contained_in_all_foods = False

                    if contained_in_all_foods:
                        responsible_ingredients.append(ingredient)

                if len(responsible_ingredients) == 1:
                    responsible_ingredient = responsible_ingredients[0]


            if responsible_ingredient is not None:
                changed_something = True

                print('"{}" is responsible for "{}"'.format(responsible_ingredient.name, allergen))

                # Ingredient definitely contains allergen and nothing else.
                responsible_ingredient.possible_allergens = [ allergen ]

                # No other ingredient contains allergen
                for other_ingredient in all_ingredients:
                    if other_ingredient is responsible_ingredient:
                        continue
                    if allergen in other_ingredient.possible_allergens:
                        other_ingredient.possible_allergens.remove(allergen)

                # Remove ingredient
                all_ingredients.remove(responsible_ingredient)

                # Remove allergen from food
                for food in affected_foods:
                    food.definite_allergens.remove(allergen)

                # Remove ingredient from food
                for food in all_foods:
                    if responsible_ingredient in food.ingredients:
                        food.ingredients.remove(responsible_ingredient)


    print()

    # Now we have removed all allergens and ingredients we
    # can map with certainty.
    #for ingr in all_ingredients:
    #    print('Ingredient: {}'.format(ingr))
    #for food in all_foods:
    #    print('Food: {}'.format(food))
    #for allergen in all_allergens:
    #    print('Allergen: {}'.format(allergen))
    #print()

    healthy_ingredients = [ingr for ingr in all_ingredients if len(ingr.possible_allergens) == 0]
    healthy_ingredient_names = [ingr.name for ingr in healthy_ingredients]
    print('Healty ingredient: {}'.format(healthy_ingredient_names))
    print()

    # Count number of occurrences of healthy ingredients
    healthy_occurrences = 0
    for ingr in healthy_ingredients:
        for food in all_foods:
            if ingr in food.ingredients:
                healthy_occurrences += 1
    print('Healthy ingredients occur {} times'.format(healthy_occurrences))

if __name__ == '__main__':
    main()
