(define (problem wood_collection_problem)
  (:domain wood_collection)
  (:objects
    player - actor
    tree - resource
  )
  (:init
    (close_to player tree)
    (= (inv_wood) 0)
  )
  (:goal (ach_place_table))
)