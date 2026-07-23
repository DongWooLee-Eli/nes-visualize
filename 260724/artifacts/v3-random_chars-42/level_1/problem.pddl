(define (problem place_zezroc_problem)
  (:domain place_zezroc_domain)
  (:objects)
  (:init
    (= (ach_place_zezroc) 0)
  )
  (:goal (> (ach_place_zezroc) 0))
)