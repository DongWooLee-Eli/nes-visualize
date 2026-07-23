(define (domain place_zezroc_game)
  (:requirements :strips :typing)
  (:predicates (ach_place_zezroc) (has_two_tpkhxk))

  (:action gather_tpkhxk_for_zezroc
    :parameters ()
    :precondition (and)
    :effect (has_two_tpkhxk)
  )

  (:action place_zezroc
    :parameters ()
    :precondition (and (has_two_tpkhxk))
    :effect (and (ach_place_zezroc) (not (has_two_tpkhxk)))
  )
)