(define (problem collect_wood_problem)
  (:domain collect_wood_domain)
  (:objects
    player - actor
    tree stone - resource
  )
  (:init
    (tree tree)
    (stone stone)
    (adjacent_to player tree)
    (= (inv_wood) 0)
    (= (inv_stone) 0)
    (= (inv_wood_pickaxe) 0)
    (= (inv_stone_pickaxe) 0)
    (= (inv_wood_sword) 0)
  )
  (:goal (achieved ach_make_stone_pickaxe))
)