(define (domain crafting_game)
  (:requirements :strips :numeric-fluents)
  (:predicates
    (ach_collect_sgqeje)
    (ach_make_sgqeje_wqiqzh)
  )
  (:functions
    (inv_sgqeje)
    (inv_sgqeje_wqiqzh)
  )
  (:action collect_sgqeje
    :parameters ()
    :precondition (>= (inv_sgqeje) 0)
    :effect (and (increase (inv_sgqeje) 1) (ach_collect_sgqeje))
  )
  (:action make_sgqeje_wqiqzh
    :parameters ()
    :precondition (>= (inv_sgqeje) 1)
    :effect (and (decrease (inv_sgqeje) 1) (increase (inv_sgqeje_wqiqzh) 1) (ach_make_sgqeje_wqiqzh))
  )
)