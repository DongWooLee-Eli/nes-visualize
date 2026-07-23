(define (domain place_zezroc_domain)
  (:requirements :strips :typing :numeric-fluents)
  (:functions (ach_place_zezroc))

  (:action place_zezroc
    :parameters ()
    :precondition (and)
    :effect (increase (ach_place_zezroc) 1)
  )
)