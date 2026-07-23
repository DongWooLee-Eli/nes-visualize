(define (domain collect_wood_domain)
  (:requirements :strips :typing :numeric-fluents)
  (:functions (inv_wood) (inv_wood_pickaxe) (ach_collect_wood) (ach_place_table) (ach_make_wood_pickaxe))
  (:action collect_wood
    :parameters ()
    :precondition (and)
    :effect (and (increase (inv_wood) 1) (increase (ach_collect_wood) 1))
  )
  (:action place_table
    :parameters ()
    :precondition (>= (inv_wood) 2)
    :effect (and (decrease (inv_wood) 2) (increase (ach_place_table) 1))
  )
  (:action make_wood_pickaxe
    :parameters ()
    :precondition (and (>= (inv_wood) 1) (>= (ach_place_table) 1))
    :effect (and (decrease (inv_wood) 1) (increase (inv_wood_pickaxe) 1) (increase (ach_make_wood_pickaxe) 1))
  )
)