(define (problem sgqeje_crafting_problem)
  (:domain sgqeje_crafting)
  (:init
    (= (inv_sgqeje) 0)
    (= (inv_sgqeje_bcwrvm) 0)
  )
  (:goal (ach_make_sgqeje_bcwrvm))
)