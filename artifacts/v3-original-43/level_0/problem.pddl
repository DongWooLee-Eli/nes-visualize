(define (problem collect_wood_problem)
  (:domain collect_wood_domain)
  (:objects player - actor tree - resource)
  (:init
    (wood_reachable player tree)
    (= (inv_wood) 0)
  )
  (:goal (>= (inv_wood) 1))
)