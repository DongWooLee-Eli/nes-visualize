(define (problem collect_wood_problem)
  (:domain collect_wood_domain)
  (:objects
    player - actor
    tree - resource
    ach_collect_wood - collectstatus
    ach_place_table - placestatus
  )
  (:init
    (harvestable_wood tree)
  )
  (:goal (achieved ach_place_table))
)