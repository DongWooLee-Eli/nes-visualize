(define (problem collect_tpkhxk_problem)
  (:domain collect_tpkhxk_domain)
  (:objects
    player - actor
    sgqeje - resource
    pmzjpl - cell
  )
  (:init
    (at player pmzjpl)
    (adjacent_to player sgqeje)
    (= (inv_tpkhxk) 0)
    (= (inv_sgqeje) 0)
    (= (inv_sgqeje_wqiqzh) 0)
  )
  (:goal (>= (inv_sgqeje_wqiqzh) 1))
)