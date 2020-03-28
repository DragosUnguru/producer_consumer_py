"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Lock


class Marketplace():
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producer_booths = {}
        self.consumer_carts = {}
        self.booths_locks = {}

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if producer_id in self.producer_booths:
            lock = self.booths_locks[producer_id]
            with lock:
                # Booth is full, try again later
                if len(self.producer_booths[producer_id]) >= self.queue_size_per_producer:
                    return False

                # Put product at sale
                self.producer_booths[producer_id].append(product)
        else:
            # Open booth
            self.producer_booths[producer_id] = [product]
            self.booths_locks[producer_id] = Lock()

        return True

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: String
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for producer in self.producer_booths:
            lock = self.booths_locks[producer]

            with lock:
                for selled_product in self.producer_booths[producer]:
                    if product == selled_product:
                        # Add product to cart
                        if cart_id in self.consumer_carts:
                            self.consumer_carts[cart_id].append((product, producer))
                        else:
                            self.consumer_carts[cart_id] = [(product, producer)]

                        # Remove product from producer's booth
                        self.producer_booths[producer].remove(product)

                        return True

        return False



    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: String
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # Get producer
        producer = next(i[1] for i in self.consumer_carts[cart_id] if i[0] == product)

        # Remove from cart
        self.consumer_carts[cart_id].remove((product, producer))

        # Put product back in the producer's booth
        lock = self.booths_locks[producer]
        with lock:
            self.producer_booths[producer].append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: String
        :param cart_id: id cart
        """
        products = [i[0] for i in self.consumer_carts[cart_id]]
        return products
