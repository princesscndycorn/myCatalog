CONTENTS OF THIS README
------------------------


* Introduction

* Requirements

* Installation 

* Running



* 1 Introduction
-----------------

This purpose for this project is to make a webpage that will be able to Create/Update/Delete contents from a database
dynamically. The website is acting as a catalog for the fictional world of Aliens and the company Weyland Yutani & the
United States Colonial Marines. Who are in a couple of the aliens movies, and books/comics. 


* 2 Requirements
-----------------

The packages list to run this app is located in "requirements.txt". You can install them manually or run the follow to 
have pip install automatically.

	* pip install -r requirements.txt


* 3 Installation
-----------------

Other than installing the above requirnments. You don't need to install anything to have the program run. You will have to run "databaseSetup.py" file and the "addCategoryitems.py" if the "waylandDatabase.db" does not exist. 

	* If "waylandDatabase.db" does not exist:
	------------------------------------------
		1. To setup the database run: python databaseSetup.py
		2. To add some basic items to database run: python addCategoryitems.py

	* If "waylandDatabase.db" exists:
	----------------------------------
		1. Proceed to next step.

* 4 Running
------------

To run this flask app, you need to run the following which will start a web server on localhost:8000. 

	* Running the web server:
	--------------------------
	1. python catServer.py

* API Example
--------------

To use the Catalogs API it is located at localhost:8000/api/. 

	* To list all categorys, Example: localhost:8000/api/
	------------------------------------------------------
	{
	  "categorys": [
	    {
	      "id": 1, 
	      "name": "Pistols"
	    }, 
	    {
	      "id": 2, 
	      "name": "Rifles"
	    }, 
	    {
	      "id": 3, 
	      "name": "Submachines"
	    }, 
	    {
	      "id": 4, 
	      "name": "Shotguns"
	    }, 
	    {
	      "id": 5, 
	      "name": "HeavyWeapons"
	    }
	  ]
	}

	* To list Items under a category, Example: localhost:8000/api/1/
	----------------------------------------------------------------
	{
	  "items": [
	    {
	      "description": "Based on the Colt M1911. The standard issue sidearm for the USCM. \n\tHolds 12 rounds. Offers greater accuracy and firepower than other pistols but at \n\ta reduced rate of fire.", 
	      "id": 1, 
	      "name": "Armat M4A3 Service Pistol"
	    }, 
	    {
	      "description": "Based on the Heckler & Koch VP70. Constructed from nano-bound, hard impact plastics and other synthetic materials. Holds 18 rounds. Lower damage than the M4A3 but a higher rate of fire, and can be modified to full-auto.", 
	      "id": 13, 
	      "name": "W-Y 88 Mod 4 Combat Pistol"
	    }
	  ]
	}

	* To list a single item under a category, Example: localhost:8000/api/1/1/
	---------------------------------------------------------------------------
	{
	  "description": "Based on the Colt M1911. The standard issue sidearm for the USCM. \n\tHolds 12 rounds. Offers greater accuracy and firepower than other pistols but at \n\ta reduced rate of fire.", 
	  "id": 1, 
	  "name": "Armat M4A3 Service Pistol"
	}

