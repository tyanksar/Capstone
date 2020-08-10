
# IT Asset Inventory System

# 1 Introduction:

In large companies, IT assets are high in quantities, utilized by various employees scattered all around the company’s facilities. Inventory in this case is required to track down the assets and assuring accentualities in some cases.  This repo creates an app that maintains IT asset inventory. The app allows to add a list of IT assets as well as adding a list of users’ information. IT assets can then be assigned to user to ensure accountability and track down any IT asset in the system. 

# Working App:

To view a production app, it can be accessed from https://capstone-turki.herokuapp.com/
Currently there is no front end so far. But it can be utilized through API endpoints mentioned in this readme file.

# Dependencies:

For this project you need Python3 (https://www.python.org/) to be installed as well as a code editor such as Visual Studio Code (https://code.visualstudio.com/).
Make sure to install the following packages afterward:
1.	Flask
2.	Flask-Migrate
3.	Flask-Script
4.	Flask-SQL Alchemy
5.	SQL-Alchemy
6.	Flask-RESTful
7.	Gunicorn and
8.	Pyscopg2 

To install the dependencies type pip install <dependency name> in the bash command line. Example: “pip install flask”.
You also need to download and install PostgreSQL (a free open source relational database) from https://www.postgresql.org/ 

# Local Development:

The repo consists of four main python files:

1.	app.py
2.	modles.py and
3.	test_app.py
4.	manage.py

The repo is kind of hybrid, meaning that it can be used for local development and with minor changes in the code it can be used in production and hosted in the cloud as well. To set it up for local development, edit both app.py and models.py and change the variable value of ENV to ‘dev’ and then save the files.
Once done, make sure that you are in the project folder.
1. Type "source setup.sh"
2. Type "./setup.sh"
3. Type “flask run --reload” to run the application and you are set to go. The app will run in the address: http://127.0.0.1:5000.
To test the code, simply run the test_app.py by typing “python test_app.py” the test bypass the authentication process as this will be tested using Postman instead. The test should end with seventeen (17) successful endpoint test results. 

# Hosting Instructions:

As mentioned earlier, the repo is hybrid, simply follow below steps to have the code ready to be deployed in the Heroku cloud service:
1.	Make sure that the ENV variable in both app.py and models.py is set to “prod”.
2.	Create an account (free) in both Heroku.com and Github.com.
3.	Download and install Heroku CLI (https://devcenter.heroku.com/articles/heroku-cli)
4.	Make sure that the Procfile exists contains the following line: “web: gunicorn 'app:create_app(test_config=None)' --preload”
5.	In the command line type: 
    a.	“python manage.py db init”
    b.	“python manage.py db migrate”
    c.	“python manage.py db upgrade”
    d.	“git init”
    e.	“heroku login”, press any key to open your browser and start logging in.
    f.	“heroku create <your app name>”, example: “heroku create capstone-project”.
    g.	“heroku addons:create heroku-postgresql:hobby-dev --app capstone-project”.
    h.	“freeze > requirements.txt”
    i.	“heroku git:remote -a capstone-project”
    j.	“git push Heroku master”
    k.	Once the app is deployed, run migrations by running: “heroku run python manage.py db upgrade --app capstone-project”
    l. in the Herkou.com website, go to settings and set the Congig Vars as follows:
    AUTH0_DOMAIN --> fsdn-turki.us.auth0.com
    ALGORITHMS --> RS256
    API_AUDIENCE --> Capstone
With this the repo is deployed in herouku and an address will be provided. Type in “heroku open” to run the app.

# Endpoints (APIs):

There are mainly ten (10) endpoints in the app listed below. Note: replace {token} with an actual one for the curl command to work:
1.	GET ‘/inventory’

•	A list of all IT asset inventory which consists of IT assets(physical ID, type and status) and the users information (name and badge number) combined together.

•	Request Arguments: none

•	curl https://capstone-turki.herokuapp.com/inventory -H "Accept: application/json" -H "Authorization: Bearer {token}"

•	If there are no IT asset inventory it will return the following JSON text:

{
"message": "There are currently no IT asset inventory",
"status": 200,
"success": true
}

•	If there is an IT asset inventory it will return the following JSON text:

{
    "it_asset_inventory": [
        {
            "Badge_no": 111111,
            "Name": "Omar",
            "Status": "PROD",
            "Type": "Computer",
            "physical_id": "C123456"
        }
    ],
    "status": 200,
    "success": true
}

2.	POST '/inventory'

•	Assigns two records to together: an IT asset and a user.

•	Request Arguments: physical_id, badge_no

•	curl -X POST -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"physical_id":"C123456", "badge_no":"111111"}' http://127.0.0.1:5000/inventory

{
    "status": 200,
    "success": true
}

3.	GET '/assets'

•	A list of all IT assets in the database.

•	Request Arguments: none.

•	curl http://127.0.0.1:5000/assets  -H "Authorization: Bearer {token}" -H "Content-Type: application/json"

•	If there are no IT asset inventory it will return the following JSON text:

{
"message": "There are currently no IT assets",
"status": 200,
"success": true
}

•	If there is a least an IT asset, it will return the following JSON text:

{
    "it_asset": {
        "id": 46,
        "physical_id": "C123456",
        "status": "PROD",
        "type": "Computer"
    },
    "status": 200,
    "success": true
}

4.	POST '/assets'

•	Inserts a new record of an IT asset in the database.

•	Request Arguments: physical_id, type and status. 

•	curl -X POST -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"physical_id":"C123456", "type":"Computer", "status":"PROD"}' http://127.0.0.1:5000/assets

{
    "it_asset": {
        "id": 46,
        "physical_id": "C123456",
        "status": "PROD",
        "type": "Computer"
    },
    "status": 200,
    "success": true
}

5.	PATCH '/assets/<string:pid>'

•	Updates an IT asset record by physical ID.

•	Request Argument: physical_id

•	curl -X PATCH -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"status":"RTIP"}' http://127.0.0.1:5000/assets/C123456

{
    "status": 200,
    "success": true
}

6.	DELETE '/assets/<string:pid>'

•	Deletes an IT asset record by physical ID.

•	Request Argument: physical_id

•	curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {token} http://127.0.0.1:5000/assets/C123456 

{
    "status": 200,
    "success": true
}

7.	GET '/users'

•	A list of all users in the database

•	Request Arguments: none

•	curl http://127.0.0.1:5000/users  -H "Authorization: Bearer {token}" -H "Content-Type: application/json"

•	If there are no users,  it will return the following JSON text:

{
    "message": "There are currently no users",
    "status": 200,
    "success": true
}

•	If there is a least one user, it will return the following JSON text:

{
    "status": 200,
    "success": true,
    "user": {
        "badge_no": 111111,
        "id": 40,
        "name": "Omar"
    }
}

8.	POST '/users'

•	Insrets a new user in the database by badge number.

•	curl -X POST -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"name":"Omar", "badge_no":"111111"}' http://127.0.0.1:5000/users

{
    "status": 200,
    "success": true,
    "user": {
        "badge_no": 111111,
        "id": 40,
        "name": "Omar"
    }
}

9.	PATCH '/users/<int:bno>'

•	Updates a user record in the database by badge number.

•	Request Argument: badge_no

•	curl -X PATCH -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"name":"Fahd"}' http://127.0.0.1:5000/users /111111

{
    "status": 200,
    "success": true
}

10.	DELETE '/users/<int:bno>'

•	Deletes a user record by badge number.

•	Request Argument: badge_no

•	curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {token} http://127.0.0.1:5000/users/111111
{
    "status": 200,
    "success": true
}

# Authentication:

Currently there are two users created in AUTH0.com: it_asset_manager and it_asset_viewer.
The former has the authentication to perform all ten (10) actions. The later will only have access to the GET methods of the end points. 
To test their authentication, please download and install Postman, run it, import the file: “fsnd-capstone prod.postman_collection.json” from the repo and then run it. It should give a pass result of eighteen (18) scenarios. 
Below are the tokens for the both of users:

# it_asset_manager:

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRxTlpCWWZBbjFZMmtKU05vZkVHOSJ9.eyJpc3MiOiJodHRwczovL2ZzZG4tdHVya2kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMjJkNTA2NWM4NDhmMDAzN2M0MWNmNSIsImF1ZCI6IkNhcHN0b25lIiwiaWF0IjoxNTk2ODY5NjY3LCJleHAiOjE1OTY5NTYwNjcsImF6cCI6IkJlWXUzVEw1TFNKVk5JMFFSNEdTWUNJb1lWVDVnZFhLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6aXRfYXNzZXQiLCJkZWxldGU6dXNlciIsImdldDppdF9hc3NldF9pbnZlbnRvcnkiLCJnZXQ6aXRfYXNzZXRzIiwiZ2V0OnVzZXJzIiwicGF0Y2g6aXRfYXNzZXQiLCJwYXRjaDp1c2VyIiwicG9zdDppdF9hc3NldCIsInBvc3Q6aXRfYXNzZXRfaW52ZW50b3J5IiwicG9zdDp1c2VyIl19.VItg9SwqZr1ewaHmsrBLTp5f_Vsf9BEhZYv1ck7KqazdKr1_exEdqGCGIdYmyM5gKarBeRbnOb1CMACFlhHAocvIx7cMpEl1mjCJ7nKotf2C5yCja35CTtE0twdjDhi-Ub5OHbMc-mBaj8yOUaHy_BnVm-FRcRlUZ8pHKlfJ-cuYbIqkgpXZp7QykLfCdxxMZV4SNVQQ6nuoVsRfsuUjJVo3jO6pP_xrZFprQ0oE4UqR1wDvl_unVxE3TrbRWsWwmNIJBkjvmoPeVE2bXHo4VB8pZuV_fwMiXQLlYIf-jvpudERnLAzbIeZS1pWrAw3tifiR6OD9zlGipqNog-PpfA

it_asset_viewer:

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRxTlpCWWZBbjFZMmtKU05vZkVHOSJ9.eyJpc3MiOiJodHRwczovL2ZzZG4tdHVya2kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMjJkNTU0MjU3YjAwMDAzOGU0Mjk3MiIsImF1ZCI6IkNhcHN0b25lIiwiaWF0IjoxNTk2ODcwMDA5LCJleHAiOjE1OTY5NTY0MDksImF6cCI6IkJlWXUzVEw1TFNKVk5JMFFSNEdTWUNJb1lWVDVnZFhLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6aXRfYXNzZXRfaW52ZW50b3J5IiwiZ2V0Oml0X2Fzc2V0cyIsImdldDp1c2VycyJdfQ.J4ZTb0F3EDDWZx2X0eTEq_hUyqZFxP79HoC-FLvwL-LU-03lEAyuF1X6pe01oevvW8c7xQOS1f5QyRbKaQ-AbpIAV0pRugwR1xfBgPLFePP1KMtXrYhpOXR2Ua2TyUwXRBz5hZAFOBNkx04jiMP_jdGXGThyohuLH0FGqvMkNoSM5CE3oSYcVEjEf9ERTlTrgkV2BtICSiWMH3PELXMUl3h-d7uXeiE9XH9kx7-efKMmsA_KCFYwewRIf3n-4b528aJrCloYper8by0tiXXM0uyCkiZA2Swrmci6eoeqMRE2a-FynltWbYht9tgjolNoIZqBz__ou8XT-H0bOcjGRg





