(define (problem collect_wood_problem)
  (:domain collect_wood_domain)
  (:objects)
  (:init
    (= (inv_wood) 0)
    (= (ach_place_table) 0)
  )
  (:goal (> (ach_place_table) 0))
)