import networkx as nx
import matplotlib.pyplot as plt
from saute.graph import *
from saute.units import UnitType, UnitValue

if __name__ == "__main__":
    cooking_graph = CookingGraph()

    flour = cooking_graph.add_ingredient("flour", 500, "grams", UnitType.WEIGHT)
    water = cooking_graph.add_ingredient("water", 300, "milliliters", UnitType.VOLUME)
    salt = cooking_graph.add_ingredient("salt", 10, "grams", UnitType.WEIGHT)

    mixing_bowl = cooking_graph.add_equipment("mixing bowl")
    whisk = cooking_graph.add_equipment("whisk")
    oven = cooking_graph.add_equipment("oven")
    baking_sheet = cooking_graph.add_equipment("baking_sheet")

    dough, remaining_ingredients = cooking_graph.add_operation(
        name="mix ingredients",
        description="Mix flour, water, and salt to form dough",
        duration=5,
        duration_unit="minutes",
        inputs={
            flour: UnitValue(400, "grams", UnitType.WEIGHT),
            water: UnitValue(250, "milliliters", UnitType.VOLUME),
            salt: UnitValue(5, "grams", UnitType.WEIGHT),
        },
        equipment=[mixing_bowl, whisk],
        product_name="dough",
        product_quantity=500,
        product_unit="grams",
        product_unit_type=UnitType.WEIGHT,
    )

    preheat_oven, _ = cooking_graph.add_operation(
        name="preheat_oven",
        description="Preheat oven to 400",
        duration=25,
        duration_unit="minutes",
        inputs={},
        equipment=[oven],
        product_name="preheated oven",
        product_quantity=400,
        product_unit="fahrenheit",
        product_unit_type=UnitType.TEMPERATURE,
    )

    bread, _ = cooking_graph.add_operation(
            name="Bake",
            description="Place dough on baking sheet and bake in oven",
            duration=30,
            duration_unit="minutes",
            inputs = {preheat_oven: UnitValue(400, "fahrenheit", UnitType.TEMPERATURE),
                      dough: UnitValue(500, "grams", UnitType.WEIGHT)},
            equipment=[baking_sheet],
            product_name="bread",
            product_quantity=500,
            product_unit="grams",
            product_unit_type=UnitType.WEIGHT,
    )

    print("\n--- Graph Representation ---")
    cooking_graph.display()

    print("\n--- Remaining Ingredients ---")
    for ingredient in remaining_ingredients:
        print(ingredient)

    print("\n--- Produced Product ---")
    print(bread)

    G = cooking_graph.graph
    for layer, nodes in enumerate(nx.topological_generations(G)):
        # `multipartite_layout` expects the layer as a node attribute, so add the
        # numeric layer value as a node attribute
        for node in nodes:
            G.nodes[node]["layer"] = layer

    # Compute the multipartite_layout using the "layer" node attribute
    #pos = nx.multipartite_layout(G, subset_key="layer")
    pos = nx.spring_layout(G)
    ingredient_list = [n for n in G.nodes() if isinstance(n, Ingredient)]
    operation_list = [n for n in G.nodes() if isinstance(n, Operation)]
    equipment_list = [n for n in G.nodes() if isinstance(n, Equipment)]

    fig, ax = plt.subplots()
    nx.draw_networkx(G, pos=pos, ax=ax, arrows=True)
    nx.draw_networkx_nodes(G, pos, nodelist=ingredient_list, node_color='blue', label='Ingredients')
    nx.draw_networkx_nodes(G, pos, nodelist=operation_list, node_color='red', label='Operations')
    nx.draw_networkx_nodes(G, pos, nodelist=equipment_list, node_color='orange', label='equipment')
    ax.set_title("DAG layout in topological order")
    fig.tight_layout()
    plt.show()
