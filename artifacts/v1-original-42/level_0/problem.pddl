(define (problem collect_wood_problem)
  (:domain collect_wood_domain)
  (:objects
    player - actor
    tree - resource
    ach_collect_wood - status
  )
  (:init
    (adjacent_to player tree)
  )
  (:goal (achieved ach_collect_wood))
)