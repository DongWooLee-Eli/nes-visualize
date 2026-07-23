(define (problem make_wood_tools_problem)
  (:domain make_wood_tools_domain)
  (:objects
    player - actor
    tree stone - source
    ach_place_table ach_make_wood_pickaxe ach_place_stone - status
  )
  (:init
    (wood_accessible player tree)
    (stone_accessible player stone)
    (= (inv_wood) 0)
    (= (inv_stone) 0)
    (= (inv_wood_pickaxe) 0)
  )
  (:goal (is_set ach_place_stone))
)