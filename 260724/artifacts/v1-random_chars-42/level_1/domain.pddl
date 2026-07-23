(define (domain place_zezroc_domain)
  (:requirements :strips :typing :negative-preconditions)
  (:types achievement)
  (:predicates (is_achieved ?result - achievement))

  (:action place_zezroc
    :parameters (?result - achievement)
    :precondition (not (is_achieved ?result))
    :effect (is_achieved ?result)
  )
)