(define (domain collect_wood_domain)
  (:requirements :strips :typing)
  (:types actor resource achievement)
  (:predicates
    (adjacent_to ?who - actor ?target - resource)
    (achieved ?result - achievement)
  )
  (:action collect_wood
    :parameters (?who - actor ?target - resource ?result - achievement)
    :precondition (adjacent_to ?who ?target)
    :effect (achieved ?result)
  )
)