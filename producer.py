"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.name = kwargs.get('name', "prod")
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.__dict__.update(kwargs)

    def run(self):
        while True:
            for product_details in self.products:
                # Get product details
                product = product_details[0]
                qty = product_details[1]
                wait_time = product_details[2]

                while qty > 0:
                    ret = self.marketplace.publish(producer_id=self.name, product=product)
                    if ret:
                        qty -= 1
                        time.sleep(wait_time)
                    else:
                        time.sleep(self.republish_wait_time)
