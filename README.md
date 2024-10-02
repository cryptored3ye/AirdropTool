# AirdropTool
A Python GUI application to manage airdrops based on LP token holdings in XRP Ledger AMM pools. Features fetching LP token holders, displaying balances and percentage shares, exporting data to CSV, and calculating airdrop allocations (distribution feature not fully tested). Includes configuration management and a user-friendly interface.



Airdrop Tool GUI for XRP Ledger AMM Pools

A Python GUI application to manage airdrops based on Liquidity Provider (LP) token holdings in Automated Market Maker (AMM) pools on the XRP Ledger.

Features
LP Token Holders Retrieval

Fetches LP token holders from a specified AMM pool.
Displays holders' account addresses, LP token balances, and their percentage share of the total LP tokens.
Allows exporting of LP token holders' data to a CSV file.
Airdrop Calculation

Calculates airdrop allocations proportionally based on LP token holdings.
Saves airdrop allocation data to a CSV file for transparency and record-keeping.
Airdrop Distribution (Untested)

Simulates the distribution of tokens to LP holders.
Note: The airdrop distribution functionality has not been fully tested. Users should exercise caution and thoroughly test this feature before using it in a production environment.
Configuration Management

Load and save airdrop configurations, including issuer address, secret key, network selection, total airdrop amount, token currency, snapshot date, and AMM pool address.
Supports multiple configurations for different airdrop campaigns.
User-Friendly GUI

Built with Tkinter for a responsive and intuitive interface.
Resizable sections with a PanedWindow layout to adjust the view between log output and LP token holders information.
Real-time logs to monitor the application's operations and catch any errors.
Getting Started
Prerequisites
Python 3.7 or higher

Ensure you have Python installed. You can download it from python.org.

Required Python Packages

Install the necessary packages using pip:


pip install xrpl-py tkinter pyyaml
Note: On some systems, tkinter is included with Python. If not, you may need to install it separately.

Installation
Clone the Repository

git clone https://github.com/poz-build/your-repository-name.git
cd your-repository-name
Run the Application

python airdrop_gui.py
Usage
Configuration Management
Load Configuration

Click on the "Load Config" button.
Select a YAML configuration file containing your airdrop settings.
Save Configuration

After entering your settings, click on the "Save Config" button to save them to a YAML file for future use.
Update Pool Info
Click on the "Update Pool Info" button to retrieve the latest LP token holders from the specified AMM pool.
The LP holders will be displayed in the LP Token Holders section, showing their account addresses, LP token balances, and percentage shares.
Calculate Airdrop
Enter Airdrop Details

Total Airdrop Amount: Specify the total number of tokens to be distributed.
Token Currency: Enter the currency symbol of the token being airdropped.
Run Calculation

Click on the "Calculate Airdrop" button.
The application will compute the airdrop allocations based on each holder's LP token balance.
Allocations are saved to airdrop_allocations.csv.
Distribute Airdrop (Untested)

Click on the "Distribute Airdrop" button to simulate the distribution of tokens to LP holders.
Warning: This feature is currently untested. Ensure thorough testing in a safe environment before deploying.
Export Data

Click on the "Save as CSV" button to export the LP token holders' data for further analysis or record-keeping.
Important Notes
Airdrop Distribution Functionality

The airdrop distribution feature is currently a simulation and has not been fully tested with actual transactions on the XRP Ledger.
Implement proper security measures and thoroughly test this functionality in a safe environment before using it in production.
Security Considerations

Never commit or share your secret keys. Ensure that secret keys are handled securely and not exposed in code repositories or logs.
Use environment variables or secure configuration management for sensitive information.
Error Handling

The application includes error handling to manage issues during data retrieval, calculations, and distribution.
Real-time logs are available to help identify and troubleshoot any errors.
Contributing
Contributions are welcome! If you encounter issues or have suggestions for improvements, please open an issue or submit a pull request.

License
This project is licensed under the MIT License.

Disclaimer
This application is provided "as is" without any warranties of any kind. The developers are not responsible for any loss or damage caused by the use of this application. Users are advised to thoroughly test the application and ensure compliance with all applicable laws and regulations before deploying it in a production environment.

Feel free to customize this README to better fit your repository or to add any additional information relevant to your project.

Additional Recommendations
Screenshots

Adding screenshots of your GUI can greatly enhance the README by providing a visual overview of the application.


## Screenshots

![Airdrop GUI Screenshot](screenshots/airdrop_gui.png)
Make sure to create a screenshots directory in your repository and add relevant images.

Changelog

Maintaining a changelog helps users track the evolution of your project.


## Changelog

See [CHANGELOG.md](CHANGELOG.md) for more information.
Contact Information

Providing a way for users to reach out can be beneficial.

## Contact

- **GitHub:** [@your-username](https://github.com/your-username)
- **Email:** [your-email@example.com](mailto:your-email@example.com)
Contribution Guidelines

Encourage contributions by outlining how others can contribute.

## Contribution

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request
Environment Variables for Security

Instead of storing sensitive information in configuration files, consider using environment variables.

## Security

- **Secret Keys:** Do not store secret keys in configuration files. Use environment variables or secure secret management solutions.
Testing Instructions

Since the airdrop distribution feature is untested, provide instructions or notes on how users can test it safely.

## Testing

The airdrop distribution feature is currently in development and has not been fully tested. Users are encouraged to test this feature in a controlled environment before using it in production.
