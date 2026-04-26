(defun string-palindrome ()
  (format t "Enter a string: ")
  (setq str (read-line))
  
  (setq rev (coerce (reverse (coerce str 'list)) 'string))
  
  (if (string-equal str rev)
      (format t "Palindrome")
      (format t "Not Palindrome"))
  
  (values))