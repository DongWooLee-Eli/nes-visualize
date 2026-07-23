(define (problem sgqeje_wqiqzh_problem)
  (:domain sgqeje_wqiqzh_domain)
  (:objects
    sgqeje - resource
    ach_make_sgqeje_wqiqzh - status
  )
  (:init
    (available sgqeje)
    (= (inv_sgqeje) 0)
  )
  (:goal (is_set ach_make_sgqeje_wqiqzh))
)