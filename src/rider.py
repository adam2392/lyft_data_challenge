import copy
from enum import Enum

import numpy as np


class FareTypes(Enum):
    BASEFEE = 2.0
    SERVICEFEE = 1.75
    MINFARE = 5.0
    PERMILE = 1.15
    PERMIN = 0.22
    MAXFARE = 400
    LYFTCUT = 0.2


class Fare(object):
    def __init__(self, primetime: bool):
        # fare is 0 -> base + sevice fee
        self.fare = 0.0
        self.mileage_total = 0
        self.time_total = 0
        self.primetime = primetime
        self.mileage_percentage = None
        self.time_percentage = None
        self._prefare = None
        if primetime < 0.0:
            raise RuntimeError("Primetime is > 0 always.")

    def __repr__(self):
        return self.fare

    def add_mile(self, leftover_miles=0):
        if leftover_miles > 0 and leftover_miles > 1:
            raise ValueError("leftovermiles can't be greater then 1...")

        if leftover_miles > 0:
            self.fare += FareTypes.PERMILE.value * leftover_miles
            self.mileage_total += FareTypes.PERMILE.value * leftover_miles
        else:
            self.fare += FareTypes.PERMILE.value
            self.mileage_total += FareTypes.PERMILE.value

    def add_minute(self, leftover_mins=0):
        if leftover_mins > 0 and leftover_mins > 1:
            raise ValueError("leftovermins can't be greater then 1...")

        if leftover_mins > 0:
            self.fare += FareTypes.PERMIN.value * leftover_mins
            self.time_total += FareTypes.PERMIN.value * leftover_mins
        else:
            self.fare += FareTypes.PERMIN.value
            self.time_total += FareTypes.PERMIN.value

    def apply_primetime(self, primetime):
        # apply primetime if it > 0
        self.fare *= (1 + self.primetime)
        self._prefare = self.fare

    def get_total(self):
        # compute fare stats after primetime is applied
        self.compute_fare_stats()

        # now add service fee
        self.fare += FareTypes.SERVICEFEE.value
        self.fare += FareTypes.BASEFEE.value

        # return the total fare
        if self.fare > FareTypes.MAXFARE.value:
            return FareTypes.MAXFARE.value
        elif self.fare < FareTypes.MINFARE.value:
            return FareTypes.MINFARE.value
        else:
            return self.fare

    def compute_fare_stats(self):
        """
        Helper function to compute fare statistics.

        - mileage as a % of total fare (not counting service fee)
        -

        :return:
        :rtype:
        """
        self._prefare = copy.copy(self.fare)

        self.mileage_total = np.array(self.mileage_total).astype(float)
        self._prefare = np.array(self._prefare).astype(float)
        self.time_total = np.array(self.time_total).astype(float)

        self.mileage_percentage = np.divide(self.mileage_total, self._prefare,
                                            out=np.zeros_like(self.mileage_total), where=self._prefare != 0)
        self.time_percentage = np.divide(self.time_total, self._prefare,
                                         out=np.zeros_like(self.time_total), where=self._prefare != 0)

    def get_prefare(self):
        if self._prefare == None:
            raise RuntimeError("Need to first compute fare stats.")

        return self._prefare


class Ride(object):
    def __init__(self, distance, duration, primetime, rideid=None, driverid=None):
        self.rideid = rideid
        self.driverid = driverid

        self.distance = distance
        self.duration = duration
        self.primetime = primetime

        self.fare = Fare(self.primetime)
        self.fare = self._compute_fare()
        self.lyftfee = self._compute_lyft_fee(self.prefare)

    def __repr__(self):
        return self.fare

    def _compute_lyft_fee(self, prefare):
        return FareTypes.LYFTCUT.value * prefare

    def _compute_fare(self):
        remaining_miles = self.distance % np.floor(self.distance)
        remaining_mins = self.duration % np.floor(self.duration)

        # compute mileage
        for _ in np.arange(np.floor(self.distance)):
            self.fare.add_mile()

        for _ in np.arange(np.floor(self.duration)):
            self.fare.add_minute()

        # add remainders
        self.fare.add_mile(remaining_miles)
        self.fare.add_minute(remaining_mins)

        self.fare.apply_primetime(self.primetime)
        self.fare.compute_fare_stats()
        self.prefare = self.fare.get_prefare()
        self.mileage_percentage = self.fare.mileage_percentage
        self.time_percentage = self.fare.time_percentage

        return self.fare.get_total()
