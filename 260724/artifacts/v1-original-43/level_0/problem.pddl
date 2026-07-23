(define (problem collect_wood_problem)
  (:domain collect_wood)

  (:objects
    player - actor
    tree - resource
    ach_collect_wood - status
  )

  (:init
    (reachable player tree)
  )

  (:goal (is_set ach_collect_wood))
)