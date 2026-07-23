(define (problem collect_stone_problem)
  (:domain collect_wood_domain)
  (:objects
    player - actor
    tree stone - resource
  )
  (:init
    (tree tree)
    (stone stone)
    (= (inv_wood) 0)
    (= (inv_stone) 0)
    (= (inv_wood_pickaxe) 0)
    (= (inv_wood_sword) 0)
  )
  (:goal (achieved ach_collect_stone))
)