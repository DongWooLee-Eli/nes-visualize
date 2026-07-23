(define (domain collect_wood_domain)
  (:requirements :strips :typing)
  (:types actor resource status)
  (:predicates
    (adjacent_to ?who - actor ?target - resource)
    (achieved ?flag - status)
  )
  (:action collect_wood
    :parameters (?who - actor ?target - resource ?flag - status)
    :precondition (adjacent_to ?who ?target)
    :effect (achieved ?flag)
  )
)