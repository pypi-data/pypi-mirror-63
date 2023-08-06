PERSIST QUEUE PACKAGE 


Project description 

persist-queue implements a file-based queue and a serial of sqlite3-based queues. The goals is to achieve following requirements: \

* Disk-based: each queued item should be stored in disk in case of any crash.
* Thread-safe: can be used by multi-threaded producers and multi-threaded consumers.
* Recoverable: Items can be read after process restart.
* Green-compatible: can be used in greenlet or eventlet environment.

