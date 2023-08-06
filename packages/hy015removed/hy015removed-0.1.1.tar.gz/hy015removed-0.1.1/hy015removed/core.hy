
(defmacro list-comp [el lis &optional test]
  (lif-not
    test
    `(lfor
       ~(first  lis)
       ~(second lis)
       ~el)
    `(lfor
       ~(first  lis)
       ~(second lis)
       :if ~test       
       ~el
       )))

(defmacro set-comp [el lis &optional test]
  (lif-not
    test
    `(sfor
       ~(first  lis)
       ~(second lis)
       ~el)
    `(sfor
       ~(first  lis)
       ~(second lis)
       :if ~test       
       ~el
       )))

(defmacro dict-comp [el lis &optional test]
  (lif-not
    test
    `(dfor
       ~(first  lis)
       ~(second lis)
       ~el)
    `(dfor
       ~(first  lis)
       ~(second lis)
       :if ~test       
       ~el
       )))


(defmacro apply [f arg]
  `(~f #*~arg)
  )
