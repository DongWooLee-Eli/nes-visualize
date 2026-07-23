(define (problem collect_wood_and_place_table_problem)
  (:domain collect_wood_and_place_table)
  (:objects
    player - actor
    tree grass - resource
  )
  (:init
    (reachable player tree)
    (reachable player grass)
    (available tree)
    (available grass)
    (can_place_table player)
    (= (wood_count player) 0)
  )
  (:goal (ach_place_table))
)