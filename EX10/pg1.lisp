(defun fibonacci (n)
  (if (<= n 1)
      n
      (+ (fibonacci (- n 1)) (fibonacci (- n 2)))))

(defun run-fibonacci ()
  (format t "Enter number of terms: ")
  (setq n (read))
  (dotimes (i n)
    (format t "~a " (fibonacci i))))
