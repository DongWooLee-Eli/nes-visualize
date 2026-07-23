(define (problem collect_tpkhxk_problem)
  (:domain collect_tpkhxk_domain)

  (:objects
    player - actor
    ach_collect_tpkhxk - status
  )

  (:init
    (reachable player tpkhxk)
  )

  (:goal (achieved ach_make_tpkhxk_bcwrvm))
)