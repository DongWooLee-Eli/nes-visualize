(define (domain place_stone_domain)
  (:requirements :strips :numeric-fluents)
  (:functions (inv_stone) (ach_place_stone))

  (:action collect_stone
    :parameters ()
    :precondition (= (inv_stone) 0)
    :effect (increase (inv_stone) 1)
  )

  (:action place_stone
    :parameters ()
    :precondition (>= (inv_stone) 1)
    :effect (and (decrease (inv_stone) 1) (increase (ach_place_stone) 1))
  )
)