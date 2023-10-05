
(cl:in-package :asdf)

(defsystem "navigation-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "GetRelevantPosition" :depends-on ("_package_GetRelevantPosition"))
    (:file "_package_GetRelevantPosition" :depends-on ("_package"))
  ))