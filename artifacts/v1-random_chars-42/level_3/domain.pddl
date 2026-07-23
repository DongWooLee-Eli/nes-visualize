(define (domain make_tpkhxk_wqiqzh_domain)
  (:requirements :strips :typing :negative-preconditions)
  (:types achievement)
  (:predicates (completed ?result - achievement))

  (:action make_tpkhxk_wqiqzh
    :parameters (?result - achievement)
    :precondition (not (completed ?result))
    :effect (completed ?result)
  )
)