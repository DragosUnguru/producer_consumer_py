"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.name = kwargs.get('name', "prod")
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.__dict__.update(kwargs)

    def run(self):
        cart_no = 0

        for cart in self.carts:
            # Create cart ID
            cart_id = self.name + str(cart_no)
            cart_no += 1

            for item in cart:
                operation = item['type']
                product = item['product']
                qty = item['quantity']

                # Fetch demanded quantity of current product
                while qty > 0:
                    if operation == "add":
                        ret = self.marketplace.add_to_cart(cart_id, product)

                        if not ret:
                            time.sleep(self.retry_wait_time)
                        else:
                            qty -= 1
                    else:
                        self.marketplace.remove_from_cart(cart_id, product)
                        qty -= 1

            # Shopping cart finished. Print what we've bought
            shopping_cart = self.marketplace.place_order(cart_id)
            for prod in shopping_cart:
                print(f'{self.name} bought {prod}')
