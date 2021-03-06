import os

from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

README = """
txredlock - Redis distributed locks in Python - Now with more deferreds!

**Warning**: This project is incomplete. Although you can acquire a lock through a deferred, the Deferred will still contact each Redis server one by one. I would like to change this so that it attempts to acquire locks on all Redis servers simultaneously.

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


The MIT License (MIT)

Copyright (c) 2014 SPS Commerce, Inc.
Copyright (c) 2016 Alex Vanderpot.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

setup(
	name='txredlock',
	version='1.0.8',
	packages=find_packages(),
	include_package_data=True,
	description='Redis locking mechanism',
	long_description=README,
	url='https://github.com/ajvpot/txredlock',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7'
	],
	author='alex@vanderpot.com',
	author_email='alex@vanderpot.com',
	install_requires=["redis"],
	entry_points={
		'console_scripts': [
			'redlock = redlock.cli:main',
		],
	}
)
