(define (domain sgqeje_wqiqzh_domain)
  (:requirements :strips :typing :negative-preconditions :numeric-fluents)
  (:types resource status)
  (:predicates
    (available ?material - resource)
    (is_set ?flag - status)
  )
  (:functions
    (inv_sgqeje)
  )
  (:action collect_sgqeje
    :parameters (?material - resource)
    :precondition (available ?material)
    :effect (increase (inv_sgqeje) 1)
  )
  (:action make_sgqeje_wqiqzh
    :parameters (?material - resource ?result - status)
    :precondition (and (available ?material) (>= (inv_sgqeje) 1) (not (is_set ?result)))
    :effect (and (decrease (inv_sgqeje) 1) (is_set ?result))
  )
)