# -*- coding: utf-8 -*-

"""
This script contains functionality for creating EV objects and Schedule objects.
It takes input from the Simulation script.
"""

__author__ = 'Ingrid Maria Mørch'
__email__ = 'ingrid.morch@gmail.com'


import pandas as pd
import dataframe_image as dfi


class EV:
    """
    This class contains the necessary characteristics for an EV object, representing an EV
    """

    def __init__(self, id, due_date, rpt):
        self.id = id                # To be able to sort the evs by identity
        self.due_date = due_date    # Number of days from admittance until due date / number of days parked
        self.rpt = rpt              # Remaining Processing Time. Here, how many charging hours are required before the EV is fully charged. (Assuming constant charging speed. Uniform chargers and batteries)

        self.is_charged = False     # For tracking later


class Schedule:
    """
    This class contains necessary variables and class methods to yield one schedule
    """

    def __init__(self, ev_pool):
        self.ev_pool = ev_pool

        self._num_charging_hours = 8

        # Containers / variables that will be updated by methods, and are needed across several methods
        self._time_frame = 0
        self._num_machines = 0

    @property
    def time_frame(self):
        """
        The time frame of the charging schedule is equal to the number of days until the latest due date
        of the EVs that are currently parked.
        """

        self.ev_pool.sort(key=lambda x: x.due_date, reverse=True)   # Sorts it by due date in descending order to identify the time frame
        self._time_frame = self.ev_pool[0].due_date
        self.ev_pool.sort(key=lambda x: x.id)     # Sorts it back in original order

        return self._time_frame

    def create_schedule(self):
        """For each charging schedule, the chargers are modeled as a minimized number of 'machines' in order to
        maximize charger idleness, and thereby minimize power peaks."""

        charging_journal = {}  # For recording when each ev is charged or not charged
        rpts = []
        released_evs = []
        hours = []

        for r in range(len(self.ev_pool)):
            print('Due date: ' + str(self.ev_pool[r].due_date))

        for ev in self.ev_pool:     # Storing original rpts before operations
            rpts.append(ev.rpt)

        for m in range(len(self.ev_pool)):      # The number of iterations the loop makes before breaking
            _clash = False      # Reset         # defines the number of modeled machines.
            charging_journal.clear()    # Reset
            released_evs.clear()        # Reset
            hours.clear()               # Reset

            for k in range(len(rpts)):          # Reset
                self.ev_pool[k].rpt = rpts[k]

            for k in range(len(self.ev_pool)):
                charging_journal["EV-" + str(k + 1)] = []

            self.ev_pool.sort(key=lambda x: x.due_date, reverse=True)   # Makes for more efficient for loop

            # For each hour in the entire timeframe. Made it count from 1, so k will match the due dates correctly
            for k in range(1, (self.time_frame * self._num_charging_hours) + 1):
                hours.append(k)

                for ev in self.ev_pool: # Here is where the error in the thesis code was, I have now added 1.
                    if k >= ((self.time_frame - ev.due_date) * self._num_charging_hours + 1) and ev not in released_evs:    # Release date on reverse timeline, counted in hours
                        released_evs.append(ev)     # Points to the original ev object in self.ev_pool

                # Sorting the released EVs, or rather their corresponding charging jobs, in descending order to see
                # which one of them to charge "first" (on the reversed timeline) according to the LRPT rule
                released_evs.sort(key=lambda x: x.rpt, reverse=True)

                # Attempt schedule as Pm problem, m = attempted number of machines (Not really, m start counting at 0,
                # therefore m + 1 in kode)
                if len(released_evs) < m + 1:
                    h = len(released_evs)           # Not + 1 because len starts at 1
                else:
                    h = m + 1                       # + 1 because the for loop starts m at 0

                for j in range(h):
                    if released_evs[j].rpt > 0:
                        released_evs[j].rpt -= 1    # Charged for one hour --> one less hour left to process
                        released_evs[j].is_charged = True

                self.ev_pool.sort(key=lambda x: x.id)  # Sorts it back in original order

                for ev in self.ev_pool:

                    if ev.is_charged:
                        charging_journal["EV-" + str(ev.id)].append('charge')
                        ev.is_charged = False  # Reset
                    else:
                        charging_journal["EV-" + str(ev.id)].append(' ')

            for ev in self.ev_pool:
                charging_journal["EV-" + str(ev.id)].reverse()      # Reversing the reversed timeline back
                                                                    # for correct display
            charging_journal['Hour'] = hours

            for ev in self.ev_pool:     # Schedule is feasible if all EVs are finished charging
                if ev.rpt > 0:          # when the reversed timeline reaches 0
                    _clash = True       # Otherwise, restart outer for loop with m = m + 1 (one more machine)
                    break

            if not _clash:
                self._num_machines = m + 1
                break

        if self._num_machines == 0:  # For debugging
            print('No feasible schedule is possible within the specified parameters') # Charging hours must be expanded

        print('Number of machines modeled: ' + str(self._num_machines))

        return pd.DataFrame(charging_journal).set_index('Hour')
