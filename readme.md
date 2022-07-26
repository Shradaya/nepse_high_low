# Notifier for when the Limit is reached/crossed by market price of shares

This application is used to notify the user if their required high/low has been reached for a given security.

## How to work with the application
* run: pip install -r requirements.txt
* Inside `mapper` module check if the security exist or not, if it doesn't add it as per the requirement.
* Inside the `security.csv` define the required security, providing high and low.
* run the application with as `python main.py --emails <emails>`. You can schedule it with cron job.
