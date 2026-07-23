(define (domain collect_tpkhxk_domain)
  (:requirements :strips :numeric-fluents)
  (:functions (inv_tpkhxk) (ach_collect_tpkhxk) (step_count))

  (:action move_left
    :parameters ()
    :precondition (and)
    :effect (and (increase (step_count) 1))
  )

  (:action move_right
    :parameters ()
    :precondition (and)
    :effect (and (increase (step_count) 1))
  )

  (:action move_up
    :parameters ()
    :precondition (and)
    :effect (and (increase (step_count) 1))
  )

  (:action move_down
    :parameters ()
    :precondition (and)
    :effect (and (increase (step_count) 1))
  )

  (:action do
    :parameters ()
    :precondition (and)
    :effect (and (increase (inv_tpkhxk) 1) (increase (ach_collect_tpkhxk) 1) (increase (step_count) 1))
  )
)