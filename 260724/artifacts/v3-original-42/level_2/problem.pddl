(define (problem wood_collection_problem)
  (:domain wood_collection)
  (:objects)
  (:init
    (= (inv_wood) 0)
    (= (inv_wood_pickaxe) 0)
  )
  (:goal (ach_make_wood_pickaxe))
)