# thunderpi

A Raspberry Pi-based Thunderboard Sense environmental monitor that reads BLE sensor data and stores it in a MariaDB database, with systemd service auto-start support.

## Overview

This project connects a Raspberry Pi to Silicon Labs Thunderboard Sense devices via Bluetooth Low Energy (BLE), reads environmental sensor data (temperature, humidity, CO2, VOC, UV, pressure, sound, light), and logs it to a local MariaDB database.

## Sensors Monitored

- Temperature & Humidity
- CO2 & TVOC (Air Quality)
- UV Index
- Barometric Pressure
- Ambient Light
- Sound Level

## Prerequisites

- Raspberry Pi (3B+ or newer recommended)
- Raspberry Pi OS (Raspbian)
- MariaDB/MySQL installed
- Python 3.7+
- Bluetooth enabled
- Silicon Labs Thunderboard Sense device

## Dependencies

```
bleak
mariadb
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Boon67/thunderpi.git
   cd thunderpi
   ```

2. Install Python dependencies:
   ```bash
   pip install bleak mariadb
   ```

3. Set up the database:
   ```bash
   mysql -u root -p < schema.sql
   ```
   This creates the `env` database with tables for records, assets, sites, and sub-assets.

4. Configure connection settings in `env.py`:
   ```python
   DB_USER = "environment_logger"
   DB_PASSWORD = "password"
   DB_HOST = "localhost"
   ```

5. Run manually:
   ```bash
   python env.py
   ```

## Auto-Start as Service

To run the monitor on boot:

1. Deploy the service:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

2. The systemd service configuration is in `serviceconfig.txt` / `lcddisplay.service`.

## Project Structure

```
├── env.py              # Main BLE sensor reader and DB writer
├── schema.sql          # MariaDB schema (creates DB, tables, user)
├── deploy.sh           # Service deployment script
├── serviceconfig.txt   # Systemd service configuration
└── README.md
```

## Database Schema

- `records` - Raw sensor JSON readings with timestamps
- `assets` - Asset registry
- `sites` - Site locations
- `sub_assets` - Sub-asset hierarchy

## License

MIT - see [LICENSE](LICENSE)
