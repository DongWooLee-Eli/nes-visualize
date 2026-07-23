(define (problem place_stone_problem)
  (:domain place_stone_domain)

  (:init
    (= (inv_stone) 0)
    (= (ach_place_stone) 0)
  )

  (:goal (>= (ach_place_stone) 1))
)