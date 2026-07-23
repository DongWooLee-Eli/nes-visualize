(define (problem collect_wood_problem)
  (:domain collect_wood_domain)

  (:objects
    player - actor
    tree stone - resource
  )

  (:init
    (adjacent_to player tree)
    (adjacent_to player stone)
    (tree tree)
    (stone stone)
    (= (inv_wood) 0)
    (= (inv_stone) 0)
    (= (inv_wood_pickaxe) 0)
    (= (inv_wood_sword) 0)
  )

  (:goal (achieved ach_place_stone))
)