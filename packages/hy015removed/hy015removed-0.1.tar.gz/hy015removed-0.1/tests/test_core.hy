(import [nose.tools [eq_  assert-equal assert-not-equal]])

;;(require [hy.contrib.walk [let]])

(import  [hy015removed.core [*]])
(require [hy015removed.core [*]])


(defn assert-all-equal [&rest tests]
  (reduce (fn [x y] (assert-equal x y) y)
          tests)
  None)

(defn test-core []

  (eq_
    (lfor
      x (range 10) (+ 1 x))
    (list-comp
      (+ 1 x) [x (range 10) ]   )
    )

  (eq_
    (lfor
      x (range 10) :if (= (% x 2)  1) (+ 1 x)  ) 
    (list-comp
      (+ 1 x) [x (range 10) ]  (= (% x 2)  1) )
    )


  (eq_
    (sfor
      x (range 10) (+ 1 x))
    (set-comp
      (+ 1 x) [x (range 10) ]   )
    )

  (eq_
    (sfor
      x (range 10) :if (= (% x 2)  1) (+ 1 x)  ) 
    (set-comp
      (+ 1 x) [x (range 10) ]  (= (% x 2)  1) )
    )

  (eq_
    (dfor
      x (range 10) [ x (+ 1 x)] )
    (dict-comp
      [ x (+ 1 x)]  [x (range 10) ]   )
    )

  (eq_
    (dfor
      x (range 10) :if (= (% x 2)  1)  [ x (+ 1 x)]   ) 
    (dict-comp
     [ x (+ 1 x)]  [x (range 10) ]  (= (% x 2)  1) )
    )
  

  
)
