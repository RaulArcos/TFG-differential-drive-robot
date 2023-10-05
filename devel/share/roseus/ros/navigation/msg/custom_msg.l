;; Auto-generated. Do not edit!


(when (boundp 'navigation::custom_msg)
  (if (not (find-package "NAVIGATION"))
    (make-package "NAVIGATION"))
  (shadow 'custom_msg (find-package "NAVIGATION")))
(unless (find-package "NAVIGATION::CUSTOM_MSG")
  (make-package "NAVIGATION::CUSTOM_MSG"))

(in-package "ROS")
;;//! \htmlinclude custom_msg.msg.html


(defclass navigation::custom_msg
  :super ros::object
  :slots (_id _message ))

(defmethod navigation::custom_msg
  (:init
   (&key
    ((:id __id) 0)
    ((:message __message) "")
    )
   (send-super :init)
   (setq _id (round __id))
   (setq _message (string __message))
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:serialization-length
   ()
   (+
    ;; int32 _id
    4
    ;; string _message
    4 (length _message)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _id
       (write-long _id s)
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _id
     (setq _id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get navigation::custom_msg :md5sum-) "057c93aa7db5ff04c6ea0d81ef773307")
(setf (get navigation::custom_msg :datatype-) "navigation/custom_msg")
(setf (get navigation::custom_msg :definition-)
      "int32 id
string message


")



(provide :navigation/custom_msg "057c93aa7db5ff04c6ea0d81ef773307")


