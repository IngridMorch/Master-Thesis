# Master-Thesis

## Python scripts "Simulation.py" and "Oneway_Charging_1.py":

These two Python scripts together comprise the smart charging program developed through my master's thesis, "Power Peak Shaving: How to Schedule Charging of Electric Vehicles and Organize Mutually Beneficial Vehicle to Grid (V2G)", which is a contribution to the research project NeX2G, an NMBU-led project in collaboration with Avinor AS, Statnett SF, OsloMet university, Elvia AS and Lnett AS.

The "Oneway_Charging_1.py" script is imported by the "Simulation.py" script. When "Simulation.py" is run, it yields a charging schedule as a png image for all the EVs in an EV pool. The input parameters in the code can be changed at will to explore different scenarios. This is further explained in comments in the code.


## Excel file:

This Excel file shows the calculations behind the assertion that an EV would typically need to sell between three and four discharging cycles
in order to fully cover it's charging cost. Below are some explanations for the numbers used.

Based on the average of those price variations, a Nissan Leaf with a 50 kWh battery would pay approximately 160 NOK for the full charging of an empty battery,
provided the EV is charged during the 8 hour nightly interval defined in the charging schedules in section 9.1, Charging scheduling. A PoC simulation,
2200 - 0600 hours.
            
Average night price is approximated from the lowest price during the defined nightly interval, on average over the last 14 days.
This price was multiplied with the battery size to get an approximate cost for the full charging of the battery. This is an optimistic approximation,
since the price did not stay as low during the entire interval, but there were some unusually high night prices in those 14 days that drives the uncertainty
in the opposite direction.
            
Average day / night price difference was approximated by subtracting the same approximated average nightly low price from the average highest daytime price
over the same 14 days.
            
Based on that average difference in buy price and sell price, the same EV owner could earn on average approximately 50 NOK per charging cycle sold.
In that case, three charging cycles is almost enough to cover the cost of fully charging an empty Nissan Leaf battery. Most batteries will not be completely
empty when they plug in at the parking house, and many will probably be happy with a 90% charged battery when they return. Three cycles will probably be enough
in many cases. But I said between three and four cycles to be transparent about the uncertainties of these calculations, that are only based on price variations
within 14 days.

Losses during transmission was not accounted for, since this is only meant as a rough estimate of how much volume must be sold for the electricity
remuneration post to be positive.
