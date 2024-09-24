# DNS Changer

DNS Changer v1.0.0 is a simple and user-friendly tool for changing DNS settings on Windows. Built with PyQt5 and WMI, it allows users to easily switch between predefined DNS servers or add custom DNS entries.

## Features

- **Set DNS**: Choose from a list of predefined DNS servers including Google DNS, Cloudflare DNS, Electro DNS, and Shekan DNS.
- **Add Custom DNS**: Add your own DNS servers with a user-friendly interface.
- **Remove DNS**: Easily remove DNS entries with a confirmation prompt.
- **Clear DNS**: Reset DNS settings to default.
- **Validation**: Ensures that custom DNS entries are in the correct format (X.X.X.X).

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mahdi1160/DNSChanger.git
   cd dns-changer
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python DNSChanger.py
```

## Configuration

The DNS servers are stored in a `dns_list.json` file located in the same directory as the main script. You can edit this file to add or modify DNS entries.

Example `dns_list.json`:
```json
{
    "Google": ["8.8.8.8", "8.8.4.4"],
    "Cloudflare": ["1.1.1.1", "1.0.0.1"],
    "Electro": ["78.157.42.100", "78.157.42.101"],
    "Shekan": ["178.22.122.100", "185.51.200.2"],
    "Radar Games": ["10.202.10.10", "10.202.10.10"]
}
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## Last releases
DNSChanger is currently only available on Windows

[DNSChanger v1.0.0 For Windows]([DNSChanger v1.0.0 For Windows](https://github.com/Mahdi1160/DNSChanger/releases/tag/v1.0.0)

## License


This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to all contributors and the open-source community for their support and contributions.
