(define (domain sgqeje_domain)
  (:requirements :strips :typing :numeric_fluents)
  (:types item)
  (:predicates
    (placed_sgqeje)
  )
  (:functions
    (inv_sgqeje)
  )
  (:action do
    :parameters ()
    :precondition (and)
    :effect (increase (inv_sgqeje) 1)
  )
  (:action place_sgqeje
    :parameters ()
    :precondition (>= (inv_sgqeje) 1)
    :effect (and (decrease (inv_sgqeje) 1) (placed_sgqeje))
  )
)