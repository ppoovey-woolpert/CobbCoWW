# README

### This is a manual "branch" of the CityofColumbiaWW repo.  Hopefully temporary. 
All the different "customers" in PRISM have their own API keys, so Columbia, Rockdale, and now Cobb all have to be kept separate (for the most part).
One pretty big wrench was that PRISM does not validate locationIDs, so as long as the API connects you will get a 202 response.  500 error otherwise. 
Lastly, Customers obviously can have conflicting locationIDs, i.e., a locationID 69 can exist for multiple customers, and the app does not currently differentiate between the customers by it's key.  Columbia's loc 69 data CAN be appended to Cobb's loc 69 if given the opportunity in this example. 

That's all for now.  This is working but will receive a refactor in the future.  contact alex.poovey if you have any questions. 


