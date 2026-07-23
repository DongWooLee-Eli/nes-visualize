(define (problem collect_tpkhxk_problem)
  (:domain collect_tpkhxk_domain)
  (:objects
    player - actor
  )
  (:init
    (= (inv_tpkhxk) 0)
    (= (inv_sgqeje) 0)
    (= (inv_sgqeje_bcwrvm) 0)
    (= (ach_collect_tpkhxk) 0)
    (= (ach_collect_sgqeje) 0)
    (= (ach_make_sgqeje_bcwrvm) 0)
  )
  (:goal (>= (ach_make_sgqeje_bcwrvm) 1))
)