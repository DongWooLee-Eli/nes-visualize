(define (problem collect_wood_place_table_problem)
  (:domain collect_wood_domain)

  (:objects
    player - actor
    grass tree ach_collect_wood - location
  )

  (:init
    (player_at player grass)
    (grass_at grass)
    (tree_at tree)
    (tree_at ach_collect_wood)
    (= (inv_wood) 0)
    (= (ach_collect_wood) 0)
    (= (ach_place_table) 0)
  )

  (:goal (>= (ach_place_table) 1))
)