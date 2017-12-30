from iCitizenFlaskApp.models.bill import Bill
from iCitizenFlaskApp.models.legislator import Legislator
                    
#legislators = Legislator.get_national_legislators("17 Queensboro Terrace", "East Windsor", "NJ", "08520")
#bills = Bill.get_national_bills(legislators, ["meat"])

state_legislators = Legislator.get_state_legislators("17 Queensboro Terrace", "East Windsor", "NJ", "08520")
Bill.get_state_bills(state_legislators, ["Crime"], "NJ")                