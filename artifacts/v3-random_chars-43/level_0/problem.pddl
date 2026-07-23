(define (problem collect_tpkhxk_problem)
  (:domain collect_tpkhxk_domain)
  (:objects player - actor xcvkpr - resource)
  (:init
    (adjacent_to player xcvkpr)
    (= (inv_tpkhxk) 0)
  )
  (:goal (>= (inv_tpkhxk) 1))
)