(define (problem make_wood_sword_problem)
  (:domain make_wood_tools_domain)
  (:objects
    player - actor
    tree - source
    ach_place_table ach_make_wood_sword - status
  )
  (:init
    (wood_accessible player tree)
    (= (inv_wood) 0)
  )
  (:goal (is_set ach_make_wood_sword))
)