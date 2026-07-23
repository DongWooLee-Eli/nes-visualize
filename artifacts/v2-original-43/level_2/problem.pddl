(define (problem collect_wood_problem)
  (:domain collect_wood_domain)
  (:objects
    player - actor
    tree - resource
  )
  (:init
    (adjacent_to player tree)
    (tree tree)
    (= (inv_wood) 0)
    (= (inv_wood_pickaxe) 0)
  )
  (:goal (achieved ach_make_wood_pickaxe))
)