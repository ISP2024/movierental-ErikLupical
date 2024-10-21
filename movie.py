import logging
from abc import ABC, abstractmethod

class PriceStrategy(ABC):
    """Abstract base class for rental pricing."""
    _instances = {}

    def __new__(cls, *args, **kwargs):
        """Override __new__ to implement singleton behavior."""
        if cls not in cls._instances:
            instance = super().__new__(cls, *args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    @abstractmethod
    def get_price(self, days: int) -> float:
        """The price of this movie rental."""
        pass

    @abstractmethod
    def get_rental_points(self, days: int) -> int:
        """The frequent renter points earned for this rental."""
        pass

class NewRelease(PriceStrategy):
    """Pricing rules for New Release movies."""

    def get_rental_points(self, days):
        """New release rentals earn 1 point for each day rented."""
        return days
    
    def get_price(self, days):
        """New release rentals are charged $3 per day."""
        return 3 * days
    
class RegularPrice(PriceStrategy):
    """Pricing rules for Regular priced movies."""

    def get_rental_points(self, days):
        """Regular movies earn 1 rental point regardless of days."""
        return 1
    
    def get_price(self, days):
        """Regular movies are charged $2 for 2 days, then $1.50 for additional days."""
        price = 2.0
        if days > 2:
            price += 1.5 * (days - 2)
        return price

class ChildrensPrice(PriceStrategy):
    """Pricing rules for Children’s movies."""

    def get_rental_points(self, days):
        """Children’s movies earn 1 rental point regardless of days."""
        return 1
    
    def get_price(self, days):
        """Children’s movies are charged $1.50 for 3 days, then $1.50 for additional days."""
        price = 1.5
        if days > 3:
            price += 1.5 * (days - 3)
        return price


class Movie:
    """
    A movie available for rent.
    """
    # The types of movies (price_code). 
    # REGULAR = 0
    # NEW_RELEASE = 1
    # CHILDRENS = 2

    REGULAR = RegularPrice()
    NEW_RELEASE = NewRelease()
    CHILDRENS =  ChildrensPrice()
    
    def __init__(self, title, price_code):
        # Initialize a new movie. 
        self.title = title
        self.price_code = price_code

    def get_price_code(self):
        # get the price code
        return self.price_code
    
    def get_title(self):
        return self.title
    
    def get_rental_points(self, days):
        # compute the frequent renter points based on movie price code
        return self.price_code.get_rental_points(days)

    def get_price(self, days):
        """Get the price of the rental."""
        if self.price_code in [Movie.REGULAR, Movie.NEW_RELEASE, Movie.CHILDRENS]:
            return self.price_code.get_price(days)
        else:
            log = logging.getLogger()
            log.error(f"Movie {self.get_movie()} has unrecognized priceCode {self.get_movie().get_price_code()}")
            
    def __str__(self):
        return self.title
