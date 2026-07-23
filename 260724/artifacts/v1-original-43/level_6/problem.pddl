(define (problem make_stone_pickaxe_problem)
  (:domain craft_minimal)

  (:objects
    tree stone - resource
    inv_wood inv_stone inv_wood_pickaxe inv_stone_pickaxe - inventory
    ach_place_table ach_make_stone_pickaxe - achievement
  )

  (:init
    (available tree)
    (available stone)
    (= (amount inv_wood) 0)
    (= (amount inv_stone) 0)
    (= (amount inv_wood_pickaxe) 0)
    (= (amount inv_stone_pickaxe) 0)
  )

  (:goal (is_set ach_make_stone_pickaxe))
)