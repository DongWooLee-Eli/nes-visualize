(define (domain collect_wood)
  (:requirements :strips :typing :negative-preconditions)
  (:types actor resource status)
  (:predicates
    (reachable ?who - actor ?target - resource)
    (close_to ?who - actor ?target - resource)
    (is_set ?flag - status)
  )

  (:action approach_tree
    :parameters (?who - actor ?target - resource)
    :precondition (reachable ?who ?target)
    :effect (close_to ?who ?target)
  )

  (:action collect
    :parameters (?who - actor ?target - resource ?result - status)
    :precondition (and (close_to ?who ?target) (not (is_set ?result)))
    :effect (is_set ?result)
  )
)