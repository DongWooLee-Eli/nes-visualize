(define (problem collect_wood_problem)
  (:domain collect_wood_domain)
  (:objects player - actor tree - resource)
  (:init
    (close_to player tree)
    (= (inv_wood) 0)
  )
  (:goal (>= (inv_wood) 1))
)