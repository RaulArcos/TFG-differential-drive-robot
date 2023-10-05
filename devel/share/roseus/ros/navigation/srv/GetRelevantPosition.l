;; Auto-generated. Do not edit!


(when (boundp 'navigation::GetRelevantPosition)
  (if (not (find-package "NAVIGATION"))
    (make-package "NAVIGATION"))
  (shadow 'GetRelevantPosition (find-package "NAVIGATION")))
(unless (find-package "NAVIGATION::GETRELEVANTPOSITION")
  (make-package "NAVIGATION::GETRELEVANTPOSITION"))
(unless (find-package "NAVIGATION::GETRELEVANTPOSITIONREQUEST")
  (make-package "NAVIGATION::GETRELEVANTPOSITIONREQUEST"))
(unless (find-package "NAVIGATION::GETRELEVANTPOSITIONRESPONSE")
  (make-package "NAVIGATION::GETRELEVANTPOSITIONRESPONSE"))

(in-package "ROS")





(defclass navigation::GetRelevantPositionRequest
  :super ros::object
  :slots (_relevantposition ))

(defmethod navigation::GetRelevantPositionRequest
  (:init
   (&key
    ((:relevantposition __relevantposition) 0)
    )
   (send-super :init)
   (setq _relevantposition (round __relevantposition))
   self)
  (:relevantposition
   (&optional __relevantposition)
   (if __relevantposition (setq _relevantposition __relevantposition)) _relevantposition)
  (:serialization-length
   ()
   (+
    ;; int32 _relevantposition
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _relevantposition
       (write-long _relevantposition s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _relevantposition
     (setq _relevantposition (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass navigation::GetRelevantPositionResponse
  :super ros::object
  :slots (_status ))

(defmethod navigation::GetRelevantPositionResponse
  (:init
   (&key
    ((:status __status) nil)
    )
   (send-super :init)
   (setq _status __status)
   self)
  (:status
   (&optional __status)
   (if __status (setq _status __status)) _status)
  (:serialization-length
   ()
   (+
    ;; bool _status
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _status
       (if _status (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _status
     (setq _status (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass navigation::GetRelevantPosition
  :super ros::object
  :slots ())

(setf (get navigation::GetRelevantPosition :md5sum-) "29c913f5cf74fb9a7ace0f16e99a4a40")
(setf (get navigation::GetRelevantPosition :datatype-) "navigation/GetRelevantPosition")
(setf (get navigation::GetRelevantPosition :request) navigation::GetRelevantPositionRequest)
(setf (get navigation::GetRelevantPosition :response) navigation::GetRelevantPositionResponse)

(defmethod navigation::GetRelevantPositionRequest
  (:response () (instance navigation::GetRelevantPositionResponse :init)))

(setf (get navigation::GetRelevantPositionRequest :md5sum-) "29c913f5cf74fb9a7ace0f16e99a4a40")
(setf (get navigation::GetRelevantPositionRequest :datatype-) "navigation/GetRelevantPositionRequest")
(setf (get navigation::GetRelevantPositionRequest :definition-)
      "int32 relevantposition
---
bool status

")

(setf (get navigation::GetRelevantPositionResponse :md5sum-) "29c913f5cf74fb9a7ace0f16e99a4a40")
(setf (get navigation::GetRelevantPositionResponse :datatype-) "navigation/GetRelevantPositionResponse")
(setf (get navigation::GetRelevantPositionResponse :definition-)
      "int32 relevantposition
---
bool status

")



(provide :navigation/GetRelevantPosition "29c913f5cf74fb9a7ace0f16e99a4a40")


