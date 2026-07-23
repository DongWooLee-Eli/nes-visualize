(define (problem collect_tpkhxk_problem)
  (:domain collect_tpkhxk_domain)
  (:objects
    player - actor
    xcvkpr - resource
    ach_collect_tpkhxk - status
  )
  (:init
    (reachable player xcvkpr)
  )
  (:goal (achieved ach_collect_tpkhxk))
)