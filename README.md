txredlock - Redis distributed locks in Python - Now with more deferreds!

**Warning**: This project is incomplete. Although you can acquire a lock through a deferred, the Deferred will still contact each Redis server one by one. I would like to change this so that it attempts to acquire locks on all Redis servers simultaneously.

ToDo
----
* Update CLI to use Twisted
* Make locks contact servers concurrently

This twisted python lib implements the Redis-based distributed lock manager algorithm [described in this blog post](http://redis.io/topics/distlock).

To create a lock manager:

	@inlineCallbacks
	def setupRedlock():
		dlm = Redlock([{"host": "localhost", "port": 6379, "db": 0}, ])
		yield dlm.connect()

To acquire a lock:

	@inlineCallbacks
	def getLock():
		my_lock = yield dlm.lock("my_resource_name",1000)

Where the resource name is an unique identifier of what you are trying to lock
and 1000 is the number of milliseconds for the validity time.

The returned value is `False` if the lock was not acquired (you may try again),
otherwise an namedtuple representing the lock is returned, having three fields:

* validity, an integer representing the number of milliseconds the lock will be valid.
* resource, the name of the locked resource as specified by the user.
* key, a random value which is used to safe reclaim the lock.

To release a lock:

	@inlineCallbacks
	def releaseLock(my_lock):
		yield dlm.unlock(my_lock)

It is possible to setup the number of retries (by default 3) and the retry
delay (by default 200 milliseconds) used to acquire the lock.


Both `dlm.lock` and `dlm.unlock` raise a exception `MultipleRedlockException` if there are errors when communicating with one or more redis masters. The caller of `dlm` should
use a try-catch-finally block to handle this exception. A `MultipleRedlockException` object
encapsulates multiple `redis-py.exceptions.RedisError` objects.


**Disclaimer**: This code implements an algorithm which is currently a proposal, it was not formally analyzed. Make sure to understand how it works before using it in your production environments.

Further Reading:
http://redis.io/topics/distlock
http://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
http://antirez.com/news/101
https://medium.com/@talentdeficit/redlock-unsafe-at-any-time-40ceac109dbb#.uj9ffh96x
