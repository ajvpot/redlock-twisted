from twisted.internet.defer import inlineCallbacks, DeferredList
from twisted.trial import unittest

from txredlock import Redlock, MultipleRedlockException, RedlockNotConnectedException


class TestRedlock(unittest.TestCase):
	@inlineCallbacks
	def setUp(self):
		self.redlock = Redlock([{}])
		yield self.redlock.connect()

	@inlineCallbacks
	def tearDown(self):
		dl = DeferredList([x.disconnect() for x in self.redlock.servers])
		yield dl

	def test_connected(self):
		self.assertGreater(len(self.redlock.servers), 0)

	@inlineCallbacks
	def test_lock(self):
		lock = yield self.redlock.lock("pants", 10000)
		self.assertEqual(lock.resource, "pants")
		yield self.redlock.unlock(lock)
		lock = yield self.redlock.lock("pants", 10000)
		self.assertEqual(lock.resource, "pants")
		yield self.redlock.unlock(lock)

	@inlineCallbacks
	def test_blocked(self):
		lock = yield self.redlock.lock("pants", 10000)
		bad = yield self.redlock.lock("pants", 10000)
		self.assertFalse(bad)
		yield self.redlock.unlock(lock)

	@inlineCallbacks
	def test_ttl_not_int_trigger_exception_value_error(self):
		with self.assertRaises(ValueError):
			yield self.redlock.lock("pants", 1000.0)

	@inlineCallbacks
	def test_not_connected_exception(self):
		rl = Redlock([{}])
		with self.assertRaises(RedlockNotConnectedException):
			yield rl.lock("pants", 10000)


	def test_multiple_redlock_exception(self):
		ex1 = Exception("Redis connection error")
		ex2 = Exception("Redis command timed out")
		exc = MultipleRedlockException([ex1, ex2])
		exc_str = str(exc)
		self.assertIn('connection error', exc_str)
		self.assertIn('command timed out', exc_str)
