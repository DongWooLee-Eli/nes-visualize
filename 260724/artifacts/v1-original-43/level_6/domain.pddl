(define (domain craft_minimal)
  (:requirements :strips :typing :numeric-fluents)
  (:types resource inventory achievement)
  (:predicates (available ?resource - resource) (is_set ?achievement - achievement))
  (:functions (amount ?inventory - inventory))

  (:action collect_wood
    :parameters (?source - resource ?wood - inventory)
    :precondition (available ?source)
    :effect (increase (amount ?wood) 1)
  )

  (:action place_table
    :parameters (?wood - inventory ?table_done - achievement)
    :precondition (>= (amount ?wood) 2)
    :effect (and (decrease (amount ?wood) 2) (is_set ?table_done))
  )

  (:action make_wood_pickaxe
    :parameters (?wood - inventory ?pickaxe - inventory ?table_done - achievement)
    :precondition (and (is_set ?table_done) (>= (amount ?wood) 1))
    :effect (and (decrease (amount ?wood) 1) (increase (amount ?pickaxe) 1))
  )

  (:action collect_stone
    :parameters (?source - resource ?pickaxe - inventory ?stone_inventory - inventory)
    :precondition (and (available ?source) (>= (amount ?pickaxe) 1))
    :effect (increase (amount ?stone_inventory) 1)
  )

  (:action make_stone_pickaxe
    :parameters (?wood - inventory ?stone_inventory - inventory ?pickaxe - inventory ?table_done - achievement ?result - achievement)
    :precondition (and (is_set ?table_done) (>= (amount ?wood) 1) (>= (amount ?stone_inventory) 1))
    :effect (and (decrease (amount ?wood) 1) (decrease (amount ?stone_inventory) 1) (increase (amount ?pickaxe) 1) (is_set ?result))
  )
)