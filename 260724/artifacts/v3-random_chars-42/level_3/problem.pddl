(define (problem make_tpkhxk_wqiqzh_problem)
  (:domain make_tpkhxk_wqiqzh)
  (:objects
    player - actor
    mynbiq - source
    inv_tpkhxk - material
    inv_tpkhxk_wqiqzh - product
  )
  (:init
    (= (amount_material inv_tpkhxk) 0)
    (= (amount_product inv_tpkhxk_wqiqzh) 0)
  )
  (:goal (>= (amount_product inv_tpkhxk_wqiqzh) 1))
)