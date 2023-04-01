FridgeBuddy
FridgeBuddy is a web application for managing the contents of your fridge. With FridgeBuddy, you can easily keep track of what you have in your fridge, when it expires, and how much you have left.

The application is built using Flask, SQLAlchemy, and Bootstrap. We use HTML, CSS, and JavaScript for the frontend. The user registration and login system is secured using password hashing with generate_password_hash and check_password_hash from the Werkzeug library.

To use FridgeBuddy, simply register for an account, log in, and start adding items to your fridge. You can update and delete items as needed, and get reminders when items are about to expire.

Requirements
Python 3.x
Flask
SQLAlchemy
Werkzeug
Installation
To install FridgeBuddy, simply clone the repository and install the required dependencies:

shell
Copy code
$ git clone https://github.com/your-username/fridgebuddy.git
$ cd fridgebuddy
$ pip install -r requirements.txt
Then, create the database and run the application:

ruby
Copy code
$ python create_db.py
$ python app.py
You can then access the application at http://localhost:5000.

Contributing
Contributions are welcome! If you find a bug or have a feature request, please create an issue on GitHub. If you'd like to contribute code, please fork the repository and submit a pull request.
