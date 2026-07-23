(define (domain collect_tpkhxk_domain)
  (:requirements :strips :typing :negative-preconditions)
  (:types actor resource status placement)
  (:constants zezroc - placement tpkhxk tpkhxk_bcwrvm - resource ach_make_tpkhxk_bcwrvm - status)
  (:predicates
    (reachable ?who - actor ?target - resource)
    (ready_to_collect ?who - actor ?target - resource)
    (inventory_at_least_one ?target - resource)
    (achieved ?flag - status)
    (placed ?target - placement)
  )

  (:action approach
    :parameters (?who - actor ?target - resource)
    :precondition (reachable ?who ?target)
    :effect (ready_to_collect ?who ?target)
  )

  (:action collect
    :parameters (?who - actor ?target - resource ?flag - status)
    :precondition (and (ready_to_collect ?who ?target) (not (achieved ?flag)))
    :effect (and (inventory_at_least_one ?target) (achieved ?flag))
  )

  (:action make_tpkhxk_bcwrvm
    :parameters ()
    :precondition (and (inventory_at_least_one tpkhxk) (not (achieved ach_make_tpkhxk_bcwrvm)))
    :effect (and (not (inventory_at_least_one tpkhxk)) (inventory_at_least_one tpkhxk_bcwrvm) (achieved ach_make_tpkhxk_bcwrvm))
  )

  (:action place_zezroc
    :parameters ()
    :precondition (not (placed zezroc))
    :effect (placed zezroc)
  )
)