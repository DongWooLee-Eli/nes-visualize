(define (problem make_wood_pickaxe_problem)
  (:domain make_wood_pickaxe_domain)
  (:objects
    tree - resource
    ach_collect_wood ach_place_table ach_make_wood_pickaxe - status
  )
  (:init
    (resource_present tree)
    (= (inv_wood) 0)
  )
  (:goal (is_set ach_make_wood_pickaxe))
)