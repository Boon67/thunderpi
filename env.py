
import sys
import time
import json
import asyncio
import logging
from bleak import discover
from bleak import BleakClient
import struct
from dataclasses import dataclass
#DB Operations Module Imports
import mariadb
import sys

DB_USER="environment_logger"
DB_PASSWORD="password"
DB_HOST="localhost"
DB_PORT=3306
DB_DATABASE="environmental"
DB_TABLE="records"


WAITTIME=1 #Time to wait between calls

RED=0
GREEN=64
BLUE=64
LIGHT=15

UUID_SERVICE_GENERIC_ACCESS = "00001800-0000-1000-8000-00805f9b34fb"
UUID_SERVICE_GENERIC_ATTRIBUTE = "00001801-0000-1000-8000-00805f9b34fb"
UUID_SERVICE_DEVICE_INFORMATION = "0000180a-0000-1000-8000-00805f9b34fb"
UUID_SERVICE_BATTERY = "0000180f-0000-1000-8000-00805f9b34fb"
UUID_SERVICE_AUTOMATION_IO = "00001815-0000-1000-8000-00805f9b34fb"
UUID_SERVICE_CSC = "00001816-0000-1000-8000-00805f9b34fb"
UUID_SERVICE_ENVIRONMENT_SENSING = "0000181a-0000-1000-8000-00805f9b34fb"
UUID_SERVICE_ACCELERATION_ORIENTATION = "a4e649f4-4be5-11e5-885d-feff819cdc9f"
UUID_SERVICE_AMBIENT_LIGHT = "d24c4f4e-17a7-4548-852c-abf51127368b"
UUID_SERVICE_INDOOR_AIR_QUALITY = "efd658ae-c400-ef33-76e7-91b00019103b"
UUID_SERVICE_HALL_EFFECT = "f598dbc5-2f00-4ec5-9936-b3d1aa4f957f" # Magnetic Field Service
UUID_SERVICE_USER_INTERFACE = "fcb89c40-c600-59f3-7dc3-5ece444a401b"
UUID_SERVICE_POWER_MANAGEMENT = "ec61a454-ed00-a5e8-b8f9-de9ec026ec51"
UUID_CHARACTERISTIC_DEVICE_NAME = "00002a00-0000-1000-8000-00805f9b34fb" #Generic Access Service
UUID_CHARACTERISTIC_APPEARANCE = "00002a01-0000-1000-8000-00805f9b34fb"
UUID_CHARACTERISTIC_ATTRIBUTE_CHANGED = "00002a05-0000-1000-8000-00805f9b34fb"
UUID_CHARACTERISTIC_SYSTEM_ID = "00002a23-0000-1000-8000-00805f9b34fb"
UUID_CHARACTERISTIC_MODEL_NUMBER = "00002a24-0000-1000-8000-00805f9b34fb"     # Device Information Service
UUID_CHARACTERISTIC_SERIAL_NUMBER = "00002a25-0000-1000-8000-00805f9b34fb"     #Device Information Service
UUID_CHARACTERISTIC_FIRMWARE_REVISION = "00002a26-0000-1000-8000-00805f9b34fb"
UUID_CHARACTERISTIC_HARDWARE_REVISION = "00002a27-0000-1000-8000-00805f9b34fb"
UUID_CHARACTERISTIC_MANUFACTURER_NAME = "00002a29-0000-1000-8000-00805f9b34fb"
UUID_CHARACTERISTIC_BATTERY_LEVEL = "00002a19-0000-1000-8000-00805f9b34fb" #Battery Service
UUID_CHARACTERISTIC_POWER_SOURCE = "EC61A454-ED01-A5E8-B8F9-DE9EC026EC51"
UUID_CHARACTERISTIC_CSC_CONTROL_POINT = "00002a55-0000-1000-8000-00805f9b34fb" #CSC Service
UUID_CHARACTERISTIC_CSC_MEASUREMENT = "00002a5b-0000-1000-8000-00805f9b34fb"
UUID_CHARACTERISTIC_CSC_FEATURE = "00002a5c-0000-1000-8000-00805f9b34fb"
UUID_CHARACTERISTIC_CSC_UNKNOWN = "9f70a8fc-826c-4c6f-9c72-41b81d1c9561"
UUID_CHARACTERISTIC_UV_INDEX = "00002a76-0000-1000-8000-00805f9b34fb"
UUID_CHARACTERISTIC_PRESSURE = "00002a6d-0000-1000-8000-00805f9b34fb" #Environment Service
UUID_CHARACTERISTIC_TEMPERATURE = "00002a6e-0000-1000-8000-00805f9b34fb"
UUID_CHARACTERISTIC_HUMIDITY = "00002a6f-0000-1000-8000-00805f9b34fb" #Environment Service
UUID_CHARACTERISTIC_AMBIENT_LIGHT_REACT = "c8546913-bfd9-45eb-8dde-9f8754f4a32e" # Ambient Light Service for React board
UUID_CHARACTERISTIC_AMBIENT_LIGHT_SENSE = "c8546913-bf01-45eb-8dde-9f8754f4a32e" # Ambient Light Service for Sense board
UUID_CHARACTERISTIC_SOUND_LEVEL = "c8546913-bf02-45eb-8dde-9f8754f4a32e"
UUID_CHARACTERISTIC_ENV_CONTROL_POINT = "c8546913-bf03-45eb-8dde-9f8754f4a32e"
UUID_CHARACTERISTIC_CO2_READING = "efd658ae-c401-ef33-76e7-91b00019103b"
UUID_CHARACTERISTIC_TVOC_READING = "efd658ae-c402-ef33-76e7-91b00019103b"
UUID_CHARACTERISTIC_AIR_QUALITY_CONTROL_POINT = "efd658ae-c403-ef33-76e7-91b00019103b"
UUID_CHARACTERISTIC_HALL_STATE = "f598dbc5-2f01-4ec5-9936-b3d1aa4f957f"
UUID_CHARACTERISTIC_HALL_FIELD_STRENGTH = "f598dbc5-2f02-4ec5-9936-b3d1aa4f957f"#
UUID_CHARACTERISTIC_HALL_CONTROL_POINT = "f598dbc5-2f03-4ec5-9936-b3d1aa4f957f"
UUID_CHARACTERISTIC_ACCELERATION = "c4c1f6e2-4be5-11e5-885d-feff819cdc9f" # Accelarion and Orientation Service
UUID_CHARACTERISTIC_ORIENTATION = "b7c4b694-bee3-45dd-ba9f-f3b5e994f49a"
UUID_CHARACTERISTIC_CALIBRATE = "71e30b8c-4131-4703-b0a0-b0bbba75856b"
UUID_CHARACTERISTIC_PUSH_BUTTONS = "fcb89c40-c601-59f3-7dc3-5ece444a401b"
UUID_CHARACTERISTIC_LEDS = "fcb89c40-c602-59f3-7dc3-5ece444a401b"
UUID_CHARACTERISTIC_RGB_LEDS = "fcb89c40-c603-59f3-7dc3-5ece444a401b"
UUID_CHARACTERISTIC_UI_CONTROL_POINT = "fcb89c40-c604-59f3-7dc3-5ece444a401b"
UUID_CHARACTERISTIC_DIGITAL = "00002a56-0000-1000-8000-00805f9b34fb" # Automation IO Service
UUID_DESCRIPTOR_CLIENT_CHARACTERISTIC_CONFIGURATION = "00002902-0000-1000-8000-00805f9b34fb" # Descriptors
UUID_DESCRIPTOR_CHARACTERISTIC_PRESENTATION_FORMAT = "00002904-0000-1000-8000-00805f9b34fb"



@dataclass
class SensorData:
    id:str=""
    temp:float=0
    humidity:float=0
    co2:float=0
    voc:float=0
    uv:float=0
    luminosity:float=0
    pressure:float=0
    sound:float=0
        
def db_submitRecord(record):
    try:
        conn = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()
    cur.execute("INSERT INTO " + DB_TABLE + " (record) VALUES (?)", (record,))
    conn.commit()
    conn.close()    

async def readThunderboards():
    devices = await discover()
    try:
        for d in devices:
            if "Thunder Sense" in d.name:
                print(d.name + '::' + d.address ) 
                await list_Services(d.address, d.name, False)
    finally:
        pass

async def list_Services(address, name, debug=False):
    log = logging.getLogger(__name__)
    if debug:
        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)

    async with BleakClient(address) as client:
        x = await client.is_connected()
        data=SensorData()
        data.id=name
        log.info("Connected: {0}".format(x))
        #value = await client.read_gatt_char(UUID_CHARACTERISTIC_RGB_LEDS)
        
        #print("LED Data Value: {0}".format(value))
        COLOR=bytearray([LIGHT,RED,GREEN,BLUE])
        #print(COLOR)
        await client.write_gatt_char(UUID_CHARACTERISTIC_RGB_LEDS, COLOR)
        data.uv=ord(await client.read_gatt_char(UUID_CHARACTERISTIC_UV_INDEX))
        data.humidity=struct.unpack('<H',await client.read_gatt_char(UUID_CHARACTERISTIC_HUMIDITY))[0] / 100
        data.temp=struct.unpack('<H',await client.read_gatt_char(UUID_CHARACTERISTIC_TEMPERATURE))[0] / 100
        data.pressure=struct.unpack('<L',await client.read_gatt_char(UUID_CHARACTERISTIC_PRESSURE))[0] /1000
        data.luminosity=struct.unpack('<L',await client.read_gatt_char(UUID_CHARACTERISTIC_AMBIENT_LIGHT_REACT))[0] /100
        data.sound=struct.unpack('<h',await client.read_gatt_char(UUID_CHARACTERISTIC_SOUND_LEVEL))[0] / 100
        data.co2=struct.unpack('<h',await client.read_gatt_char(UUID_CHARACTERISTIC_CO2_READING))[0]
        data.voc=struct.unpack('<h',await client.read_gatt_char(UUID_CHARACTERISTIC_TVOC_READING))[0]

        if await client.is_connected():
            await client.disconnect()
        print(data)
        db_submitRecord(json.dumps(data.__dict__))
print('starting....')
run=True
loop = asyncio.get_event_loop()
while run:
    try:
        loop.run_until_complete(readThunderboards())
        time.sleep(WAITTIME)
    except KeyboardInterrupt:
        run=False
        print('Done')
        
        

