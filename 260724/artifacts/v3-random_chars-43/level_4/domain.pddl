(define (domain collect_tpkhxk_domain)
  (:requirements :strips :typing :numeric-fluents)
  (:functions (inv_tpkhxk) (inv_sgqeje))
  (:action collect_tpkhxk
    :parameters ()
    :precondition (and)
    :effect (increase (inv_tpkhxk) 1)
  )
  (:action collect_sgqeje
    :parameters ()
    :precondition (and)
    :effect (increase (inv_sgqeje) 1)
  )
)