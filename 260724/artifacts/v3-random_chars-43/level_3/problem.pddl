(define (problem collect_tpkhxk_problem)
  (:domain collect_tpkhxk_domain)
  (:objects
    player - actor
  )
  (:init
    (= (inv_tpkhxk) 0)
    (= (inv_tpkhxk_wqiqzh) 0)
    (= (ach_collect_tpkhxk) 0)
    (= (ach_make_tpkhxk_wqiqzh) 0)
  )
  (:goal (>= (ach_make_tpkhxk_wqiqzh) 1))
)