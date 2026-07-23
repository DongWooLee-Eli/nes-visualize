(define (problem collect_wood_place_table_problem)
  (:domain collect_wood_domain)
  (:objects
    player - actor
    tree - resource
  )
  (:init
    (adjacent_to player tree)
    (tree tree)
    (= (inv_wood) 0)
  )
  (:goal (achieved ach_place_table))
)