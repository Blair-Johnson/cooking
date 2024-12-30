from typing import List, Dict, Tuple, Union
from .units import UnitValue, UnitType
import networkx as nx


class Ingredient:
    def __init__(self, name: str, quantity: UnitValue):
        self.name = name
        self.quantity = quantity

    def __repr__(self):
        return f"{self.quantity} of {self.name}"


class Equipment:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Equipment: {self.name}"


class Operation:
    def __init__(self, name: str, description: str, duration: UnitValue):
        self.name = name
        self.description = description
        self.duration = duration

    def __repr__(self):
        return f"Operation: {self.name} ({self.duration})"


class CookingGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.intermediate_counter = 0

    def add_ingredient(self, name: str, quantity: float, unit: str, unit_type: UnitType):
        ingredient = Ingredient(name, UnitValue(quantity, unit, unit_type))
        self.graph.add_node(ingredient)
        return ingredient

    def add_equipment(self, name: str):
        equipment = Equipment(name)
        self.graph.add_node(equipment)
        return equipment

    def add_operation(
        self,
        name: str,
        description: str,
        duration: float,
        duration_unit: str,
        inputs: Dict[Ingredient, UnitValue],
        equipment: List[Equipment],
        product_name: str = None,
        product_quantity: float = None,
        product_unit: str = None,
        product_unit_type: UnitType = None,
    ) -> Tuple[Ingredient, List[Ingredient]]:
        if product_name is None:
            product_name = f"Intermediate_{self.intermediate_counter}"
            self.intermediate_counter += 1

        if product_quantity is None or product_unit is None or product_unit_type is None:
            product_quantity, product_unit, product_unit_type = 1, "piece", UnitType.WEIGHT

        operation = Operation(
            name, description, UnitValue(duration, duration_unit, UnitType.TIME)
        )
        self.graph.add_node(operation)

        for ingredient, quantity_used in inputs.items():
            quantity_used_in_si = quantity_used.to_si()
            ingredient_in_si = ingredient.quantity.to_si()

            if ingredient.quantity.unit_type in UnitValue.CONSUMABLE:
                if ingredient_in_si < quantity_used_in_si:
                    raise ValueError(
                        f"Not enough {ingredient.name} (requires {quantity_used.value} {quantity_used.unit}, "
                        f"has {ingredient.quantity.value} {ingredient.quantity.unit})"
                    )

                remaining_quantity = ingredient_in_si - quantity_used_in_si
                ingredient.quantity = UnitValue(
                    UnitValue.CONVERT_FROM_SI[ingredient.quantity.unit_type][ingredient.quantity.unit](remaining_quantity),
                    ingredient.quantity.unit,
                    ingredient.quantity.unit_type,
                )
            self.graph.add_edge(ingredient, operation, quantity_used=quantity_used)

        for eq in equipment:
            self.graph.add_edge(eq, operation)

        product_quantity_si = UnitValue(product_quantity, product_unit, product_unit_type).to_si()
        product = Ingredient(
            product_name,
            UnitValue(
                UnitValue.CONVERT_FROM_SI[product_unit_type][product_unit](product_quantity_si),
                product_unit,
                product_unit_type,
            ),
        )
        self.graph.add_edge(operation, product)

        remaining_ingredients = [ing for ing in inputs if ing.quantity.to_si() > 0]

        return product, remaining_ingredients

    def display(self):
        for node in self.graph.nodes:
            print(node)
        for edge in self.graph.edges:
            data = self.graph.edges[edge]
            if "quantity_used" in data:
                print(f"{edge[0]} -> {edge[1]} (uses {data['quantity_used']})")
            else:
                print(f"{edge[0]} -> {edge[1]}")
