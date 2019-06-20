'''
Created on Jun 20, 2019

@author: Gabriel Torrandella
'''
import unittest
import redis

class Test(unittest.TestCase):


    def setUp(self):
        self.master = redis.from_url("redis://localhost:6379")
        self.sentinel = redis.from_url("redis://localhost:26380")
        self.pubSubOb = self.sentinel.pubsub()
        self.pubSubOb.subscribe("+sdown", "+odown", "switch-master")
        self.IP_Original_Master = self.sentinel.sentinel_master("redis-example")['ip']
        

    def tearDown(self):
        self.pubSubOb.unsubscribe()
        self.sentinel.connection_pool.disconnect()
        self.master.connection_pool.disconnect()

    def test_Master_Chan(self):
        print("Sleeping the Master for 45 seconds...")
        self.master.execute_command("DEBUG sleep 45")
            
        IP_New_Master = self.sentinel.sentinel_master("redis-example")['ip']
        self.assertNotEqual(self.IP_Original_Master, IP_New_Master)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
