# -*- coding: utf-8 -*-

"""
This script contains functionality for simulating conditions at the airport,
which gives the necessary input to the classes and class methods in the Oneway_charging script.

FUTURE ADDITION: Also gives input to a script called Twoway_charging, which accommodates V2G functionality
"""

__author__ = 'Ingrid Maria Mørch'
__email__ = 'ingrid.morch@gmail.com'


import Oneway_charging_1
# FUTURE ADDITION: import Twoway_charging

import random
import dataframe_image as dfi

#from tabulate import tabulate


class Sim_1_way:
    """
    This class defines necessary variables and class methods to create a charging schedule
    for EVs without V2G capability or willingness.
    """

    def __init__(self):

        """
        Variables of chosen size, can be changed to more feasible values. Could have made them inputs along with
        num_evs, but that would make for unnecessarily cumbersome simulations for the purposes of this thesis
        """

        self.num_charging_hours = 8  # Cheap night night time spot price on energy
        self.min_days_parked = 1
        self.max_days_parked = 3
        self.max_rpt = 6  # As many hours as it takes to fully charged an empty car battery of a chosen common size

        self.ev_pool = []   # Container for EV objects
        self.schedule = None
        self.num_days_sim = 0   # Will be updated by the input when simulation function is called
        self.num_evs_sim = 0    # Will be updated by the input when simulation function is called

    def create_ev_pool(self, num_evs_sim):
        """
        Simulates EVs with relevant characteristics and places them in the empty list self.ev_pool
        """
        ev_pool = []
        num_evs = num_evs_sim

        # rpt, remaining processing time, i.e. how depleted the battery is, should be simulated like this:
        # random.randint(self.min_rpt, self.max_rpt). They are all set to max.rpt, i.e. same charging needs,
        # for clearer example schedules in thesis

        for k in range(num_evs):
            ev = Oneway_charging_1.EV((k + 1), random.randint(self.min_days_parked, self.max_days_parked), self.max_rpt)
            ev_pool.append(ev)

        return ev_pool

    def daily_cycle(self, schedule):
        """
        Creates a schedule based on the EVs currently present in the parking house
        """
        charging_schedule = Oneway_charging_1.Schedule.create_schedule(schedule)

        return charging_schedule

    def update_ev_pool(self):
        """
        FUTURE ADDITION:
            * EVs past their due date are removed from the ev pool
            * New EVs are added

            * Return: Updated self.ev_pool
        """

    def simulate(self, num_days_sim, num_evs_sim):
        self.num_days_sim = num_days_sim
        self.num_evs_sim = num_evs_sim
        self.ev_pool = self.create_ev_pool(num_evs_sim)
        schedule = Oneway_charging_1.Schedule(self.ev_pool)

        charging_schedule = self.daily_cycle(schedule)

        # FUTURE ADDITION: self.ev_pool = update_ev_pool()

        return charging_schedule
        #return print(tabulate(charging_schedule, headers = 'keys', tablefmt = 'psql'))


class Sim_2_way:
    """
    FUTURE ADDITION:
        * Functionality from Sim_1_way class is replicated and extended to include two-way charging capability,
            i.e. V2G participation.
        * Notable extensions to EV characteristics:
            * charging cycles to sell (energy volume)

        * Notable changes to charging schedule:
            * Includes scheduling of energy sale during daytime (only which days the batteries are available)
            * Includes recharging of the same EV several times

        * Also possible to keep track of remuneration
    """

if __name__ == '__main__':
    my_schedule = Sim_1_way.simulate(Sim_1_way(), 1, 6)
    dfi.export(my_schedule, "charging_schedule.png")

#print(Sim_1_way.simulate(Sim_1_way(), 1, 6))    # Number of days must be 1 for now, before update_schedule is finished.
                                                # NOTE: This means one schedule, based on one snapshot in time.
                                                # Number of days scheduled is equal to the furthest due date of the EVs.

                                                # Number of EVs can be set to anything, depending on what scenario
                                                # one wants to explore. Here: 6

