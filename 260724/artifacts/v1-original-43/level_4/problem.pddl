(define (problem collect_stone_problem)
  (:domain make_wood_tools_domain)
  (:objects
    player - actor
    tree stone - source
    ach_place_table ach_make_wood_pickaxe - status
  )
  (:init
    (wood_accessible player tree)
    (stone_accessible player stone)
    (= (inv_wood) 0)
    (= (inv_stone) 0)
    (= (inv_wood_pickaxe) 0)
  )
  (:goal (>= (inv_stone) 1))
)