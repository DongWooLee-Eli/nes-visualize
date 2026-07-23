(define (domain tpkhxk_crafting)
  (:requirements :strips :typing :numeric-fluents)
  (:types resource)
  (:predicates (resource_available ?source - resource))
  (:functions (inv_tpkhxk) (inv_tpkhxk_bcwrvm) (ach_collect_tpkhxk) (ach_make_tpkhxk_bcwrvm))

  (:action collect_tpkhxk
    :parameters ()
    :precondition (and)
    :effect (and (increase (inv_tpkhxk) 1) (increase (ach_collect_tpkhxk) 1))
  )

  (:action make_tpkhxk_bcwrvm
    :parameters ()
    :precondition (>= (inv_tpkhxk) 3)
    :effect (and (decrease (inv_tpkhxk) 3) (increase (inv_tpkhxk_bcwrvm) 1) (increase (ach_make_tpkhxk_bcwrvm) 1))
  )
)