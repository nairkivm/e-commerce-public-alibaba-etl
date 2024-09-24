import math
import random as rd
from utils.source_requirements import SourceRequirements
from faker import Faker
from faker.providers import internet
from datetime import datetime, timedelta
import string

fake = Faker()
print('Faker ready')

class SourceData:
    def __init__(self, table_name) -> None:
        self.table_name = table_name
        self.file_name = SourceRequirements().requirements[self.table_name]['source_path']

    def append_to_file(self, text):
        with open(self.file_name, 'a') as file:
            file.write(text + '\n')

    def read_last_line(self):
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            if lines:
                return lines[-1].strip()
            else:
                return None

    def fetch_distinct_columns_values(self, column):
        with open(self.file_name, 'r', encoding='utf-8', errors='ignore') as file:
            values = []
            i = 0
            for line in file.readlines():
                if i > 0:
                    values.append(line.split('\t')[column].strip())
                i+=1
            values = list(set(values))
            return values
        
    def fetch_data(self):
        with open(self.file_name, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            keys = [str(word).strip() for word in lines[0].split('\t')]
            result = []
            i = 0
            for i in range(len(lines)):
                if i > 0:
                    values = [str(val).strip() for val in lines[i].split('\t')]
                    dict_ = {}
                    for j in range(len(keys)):
                        dict_[keys[j]] = values[j]
                    result.append(dict_)
            return result

sources = {str(table): SourceData(table) for table in SourceRequirements().requirements.keys()}

def generate_carts_has_products(rows: int):
    last_shopping_cart_id = sources['carts_has_products'].read_last_line().split('\t')[0]
    product_ids = sources['products'].fetch_distinct_columns_values(0)
    option_ids = sources['options'].fetch_distinct_columns_values(0)

    shopping_cart_ids = [int(i*100) for i in range(int(last_shopping_cart_id[:2]) + 1, math.ceil(int(last_shopping_cart_id[:2]) + (1 + rows) / 4))]
    option_ids = [x for x in option_ids if x[:2] in [x[:2] for x in product_ids]]

    generated_data = []
    for i in range(rows):
        shopping_cart_id = str(rd.choice(shopping_cart_ids))
        product_id = str(rd.choice(product_ids))
        option_id = str(rd.choice([x for x in option_ids if x[:2] == product_id[:2]]))
        quantity = str(rd.randint(1,7))
        generated_row = "\t".join([shopping_cart_id, product_id, option_id, quantity])
        generated_data.append(generated_row)
    
    generated_data = "\n".join(sorted(generated_data))
    sources['carts_has_products'].append_to_file(generated_data)

def generate_categories():
    generated_data="""\
4700	Monitors
4800	Keyboards
4900	Mice
5000	Printers
5100	Scanners
5200	Webcams
5300	Speakers
5400	Microphones
5500	External Drives
5600	Memory Cards
5700	USB Hubs
5800	Routers
5900	Switches
6000	Modems
6100	Projectors
6200	Smartwatches
6300	Fitness Trackers
6400	VR Headsets
6500	Drones
6600	Game Consoles
6700	Smart TVs
6800	Streaming Devices
6900	E-readers
7000	Smart Home Devices
7100	Security Cameras
7200	Thermostats
7300	Light Bulbs
7400	Smart Plugs
7500	Smart Locks
7600	Doorbells
7700	Smoke Detectors
7800	Carbon Monoxide Detectors
7900	Smart Speakers
8000	Smart Displays
8100	Smart Glasses
8200	Wearable Cameras
8300	Action Cameras
8400	Dash Cams
8500	Baby Monitors
8600	Pet Cameras
8700	GPS Trackers
8800	Car Chargers
8900	Car Mounts
9000	Car Audio Systems"""
    sources['categories'].append_to_file(generated_data)

def generate_products():
    generated_data="""\
2700	Dell Inspiron 15	A versatile laptop with a 15.6-inch display, Intel Core i5 processor, and 8GB RAM.
2800	HP Spectre x360 A 2-in-1 laptop with a 13.3-inch touchscreen, Intel Core i7 processor, and 16GB RAM.
2900	Samsung Galaxy S21  A high-end smartphone with a 6.2-inch display, Exynos 2100 processor, and 128GB storage.
3000	Google Pixel 5	A smartphone with a 6.0-inch OLED display, Snapdragon 765G processor, and 128GB storage.
3100	iPad Pro 11-inch	A powerful tablet with an 11-inch Liquid Retina display, A12Z Bionic chip, and 256GB storage.
3200	Microsoft Surface Pro 7	A versatile tablet with a 12.3-inch display, Intel Core i5 processor, and 8GB RAM.
3300	Lenovo ThinkPad X1 Carbon	A lightweight laptop with a 14-inch display, Intel Core i7 processor, and 16GB RAM.
3400	ASUS ROG Zephyrus G14	A gaming laptop with a 14-inch display, AMD Ryzen 9 processor, and NVIDIA GeForce RTX 2060 GPU.
3500	Bose QuietComfort 35 II	Wireless noise-cancelling headphones with up to 20 hours of battery life.
3600	Sony WH-1000XM4	Industry-leading noise-cancelling headphones with up to 30 hours of battery life.
3700	JBL Charge 4	Portable Bluetooth speaker with up to 20 hours of playtime and IPX7 waterproof rating.
3800	Amazon Echo Dot (4th Gen)	Smart speaker with Alexa and improved sound quality.
3900	Google Nest Hub Max	Smart display with a 10-inch screen and built-in Google Assistant.
4000	Fitbit Charge 4	Fitness tracker with built-in GPS, heart rate monitoring, and sleep tracking.
4100	Garmin Forerunner 245	GPS running watch with advanced training features and music storage.
4200	Oculus Quest 2	All-in-one VR headset with a high-resolution display and 64GB storage.
4300	DJI Mavic Air 2	Compact drone with 4K camera, 34-minute flight time, and advanced obstacle avoidance.
4400	PlayStation 5	Next-gen gaming console with ultra-high-speed SSD and 4K gaming capabilities.
4500	Xbox Series X	Powerful gaming console with 12 teraflops of processing power and 1TB SSD.
4600	Samsung QLED 8K TV	75-inch 8K TV with Quantum Processor 8K and AI upscaling.
4700	Roku Streaming Stick+	4K streaming device with long-range wireless and voice remote.
4800	Kindle Paperwhite	E-reader with a 6-inch high-resolution display and built-in adjustable light.
4900	Philips Hue White and Color Ambiance	Smart light bulb with 16 million colors and voice control.
5000	Ring Video Doorbell 3	Smart doorbell with 1080p HD video, motion detection, and two-way talk.
5100	Nest Learning Thermostat	Smart thermostat with auto-schedule and energy-saving features.
5200	TP-Link Kasa Smart Plug	Wi-Fi smart plug with voice control and energy monitoring.
5300	August Smart Lock Pro	Smart lock with remote access, auto-lock, and compatibility with Alexa and Google Assistant.
5400	Arlo Pro 3	Wireless security camera with 2K HDR video, color night vision, and 160-degree field of view.
5500	First Alert Smoke and CO Detector	Smart smoke and carbon monoxide detector with voice alerts and mobile notifications.
5600	Sonos One	Smart speaker with voice control and rich, room-filling sound.
5700	Lenovo Smart Clock	Smart clock with Google Assistant and 4-inch touchscreen display.
5800	Ray-Ban Stories	Smart glasses with built-in cameras and audio.
5900	GoPro HERO9 Black	Action camera with 5K video, 20MP photos, and HyperSmooth 3.0 stabilization.
6000	Garmin Dash Cam Mini	Compact dash camera with 1080p HD video and voice control.
6100	Motorola MBP36XL	Video baby monitor with 5-inch screen, remote pan, tilt, and zoom.
6200	Furbo Dog Camera	Pet camera with treat tossing, 1080p HD video, and two-way audio.
6300	Tile Pro	High-performance Bluetooth tracker with a 400-foot range and replaceable battery.
6400	Anker PowerDrive 2	Dual USB car charger with PowerIQ technology for fast charging.
6500	iOttie Easy One Touch 4	Car mount with one-touch locking mechanism and adjustable viewing angles.
6600	Pioneer AVH-2500NEX	In-dash car stereo with 7-inch touchscreen, Apple CarPlay, and Android Auto.
6700	Seagate Backup Plus Portable	External hard drive with 2TB storage and USB 3.0 connectivity.
6800	SanDisk Extreme Pro SDXC	High-performance memory card with 128GB storage and up to 170MB/s read speed.
6900	Kingston DataTraveler 100 G3	USB flash drive with 64GB storage and USB 3.0 interface.
7000	TP-Link Archer AX6000	High-speed Wi-Fi 6 router with 8-stream connectivity and advanced security features.
7100	Netgear Nighthawk X6S	Tri-band Wi-Fi router with 4x4 MU-MIMO and 3.2Gbps speed.
7200	Epson EcoTank ET-4760	All-in-one printer with cartridge-free printing and up to 2 years of ink included.
7300	Brother HL-L2350DW	Compact monochrome laser printer with wireless printing and duplex capability.
7400	Canon CanoScan LiDE400	High-resolution flatbed scanner with 4800 dpi and USB-C connectivity.
7500	Logitech C920s Pro HD Webcam	Full HD webcam with 1080p video and built-in privacy shutter."""
    sources['products'].append_to_file(generated_data)

def generate_products_belong_category():
    generated_data="""\
2100	4400
2200	4400
2300	4500
2400	4500
2500	4600
2600	4600
2700	4000
2800	4000
2900	4100
3000	4100
3100	4200
3200	4200
3300	4000
3400	4000
3500	4600
3600	4600
3700	4600
3800	4600
3900	4600
4000	6200
4100	6200
4200	6400
4300	6500
4400	6600
4500	6600
4600	6700
4700	6800
4800	6900
4900	7000
5000	7100
5100	7200
5200	7300
5300	7400
5400	7500
5500	7700
5600	7900
5700	8000
5800	8100
5900	8300
6000	8400
6100	8500
6200	8600
6300	8700
6400	8800
6500	8900
6600	9000
6700	5500
6800	5600
6900	5700
7000	5800
7100	5900
7200	6000
7300	6100
7400	6200
7500	6300"""
    sources['products_belong_category'].append_to_file(generated_data)

def generate_options():
    generated_data="""\
2701	Dell Inspiron 15 - 8GB RAM
2702	Dell Inspiron 15 - 16GB RAM
2801	HP Spectre x360 - 13.3-inch
2802	HP Spectre x360 - 15.6-inch
2901	Samsung Galaxy S21 - 128GB
2902	Samsung Galaxy S21 - 256GB
3001	Google Pixel 5 - 128GB
3002	Google Pixel 5 - 256GB
3101	iPad Pro 11-inch - 128GB
3102	iPad Pro 11-inch - 256GB
3201	Microsoft Surface Pro 7 - 128GB
3202	Microsoft Surface Pro 7 - 256GB
3301	Lenovo ThinkPad X1 Carbon - 8GB RAM
3302	Lenovo ThinkPad X1 Carbon - 16GB RAM
3401	ASUS ROG Zephyrus G14 - 16GB RAM
3402	ASUS ROG Zephyrus G14 - 32GB RAM
3501	Bose QuietComfort 35 II - Black
3502	Bose QuietComfort 35 II - Silver
3601	Sony WH-1000XM4 - Black
3602	Sony WH-1000XM4 - Silver
3701	JBL Charge 4 - Black
3702	JBL Charge 4 - Blue
3801	Amazon Echo Dot (4th Gen) - Charcoal
3802	Amazon Echo Dot (4th Gen) - Glacier White
3901	Google Nest Hub Max - Charcoal
3902	Google Nest Hub Max - Chalk
4001	Fitbit Charge 4 - Black
4002	Fitbit Charge 4 - Rosewood
4101	Garmin Forerunner 245 - Black
4102	Garmin Forerunner 245 - Aqua
4201	Oculus Quest 2 - 64GB
4202	Oculus Quest 2 - 256GB
4301	DJI Mavic Air 2 - Fly More Combo
4302	DJI Mavic Air 2 - Standard
4401	PlayStation 5 - Digital Edition
4402	PlayStation 5 - Standard Edition
4501	Xbox Series X - 1TB
4502	Xbox Series X - 2TB
4601	Samsung QLED 8K TV - 65-inch
4602	Samsung QLED 8K TV - 75-inch
4701	Roku Streaming Stick+ - Standard
4702	Roku Streaming Stick+ - 4K
4801	Kindle Paperwhite - 8GB
4802	Kindle Paperwhite - 32GB
4901	Philips Hue White and Color Ambiance - Single
4902	Philips Hue White and Color Ambiance - 2-Pack
5001	Ring Video Doorbell 3 - Standard
5002	Ring Video Doorbell 3 - Plus
5101	Nest Learning Thermostat - 3rd Gen
5102	Nest Learning Thermostat - 4th Gen
5201	TP-Link Kasa Smart Plug - Single
5202	TP-Link Kasa Smart Plug - 2-Pack
5301	August Smart Lock Pro - Silver
5302	August Smart Lock Pro - Black
5401	Arlo Pro 3 - Single Camera
5402	Arlo Pro 3 - 2-Camera Kit
5501	First Alert Smoke and CO Detector - Battery
5502	First Alert Smoke and CO Detector - Hardwired
5601	Sonos One - Black
5602	Sonos One - White
5701	Lenovo Smart Clock - Standard
5702	Lenovo Smart Clock - Essential
5801	Ray-Ban Stories - Wayfarer
5802	Ray-Ban Stories - Round
5901	GoPro HERO9 Black - Standard
5902	GoPro HERO9 Black - Bundle
6001	Garmin Dash Cam Mini - Standard
6002	Garmin Dash Cam Mini - Bundle
6101	Motorola MBP36XL - Standard
6102	Motorola MBP36XL - Deluxe
6201	Furbo Dog Camera - Standard
6202	Furbo Dog Camera - Plus
6301	Tile Pro - Black
6302	Tile Pro - White
6401	Anker PowerDrive 2 - Black
6402	Anker PowerDrive 2 - White
6501	iOttie Easy One Touch 4 - Standard
6502	iOttie Easy One Touch 4 - Deluxe
6601	Pioneer AVH-2500NEX - Standard
6602	Pioneer AVH-2500NEX - Premium
6701	Seagate Backup Plus Portable - 1TB
6702	Seagate Backup Plus Portable - 2TB
6801	SanDisk Extreme Pro SDXC - 64GB
6802	SanDisk Extreme Pro SDXC - 128GB
6901	Kingston DataTraveler 100 G3 - 32GB
6902	Kingston DataTraveler 100 G3 - 64GB
7001	TP-Link Archer AX6000 - Standard
7002	TP-Link Archer AX6000 - Pro
7101	Netgear Nighthawk X6S - Standard
7102	Netgear Nighthawk X6S - Pro
7201	Epson EcoTank ET-4760 - Standard
7202	Epson EcoTank ET-4760 - Deluxe
7301	Brother HL-L2350DW - Standard
7302	Brother HL-L2350DW - Pro
7401	Canon CanoScan LiDE400 - Standard
7402	Canon CanoScan LiDE400 - Premium
7501	Logitech C920s Pro HD Webcam - Standard
7502	Logitech C920s Pro HD Webcam - Deluxe"""
    sources['options'].append_to_file(generated_data)

def generate_products_has_options():
    generated_data="""\
2700	2701	5	800	1	Dell Inspiron 15 - 8GB RAM, 15.6-inch display, Intel Core i5 processor
2700	2702	3	1000	0	Dell Inspiron 15 - 16GB RAM, 15.6-inch display, Intel Core i7 processor
2800	2801	4	1200	1	HP Spectre x360 - 13.3-inch, Intel Core i5 processor, 8GB RAM
2800	2802	2	1400	0	HP Spectre x360 - 15.6-inch, Intel Core i7 processor, 16GB RAM
2900	2901	10	999	1	Samsung Galaxy S21 - 128GB storage, Exynos 2100 processor
2900	2902	5	1199	0	Samsung Galaxy S21 - 256GB storage, Exynos 2100 processor
3000	3001	8	799	1	Google Pixel 5 - 128GB storage, Snapdragon 765G processor
3000	3002	4	899	0	Google Pixel 5 - 256GB storage, Snapdragon 765G processor
3100	3101	6	999	1	iPad Pro 11-inch - 128GB storage, A12Z Bionic chip
3100	3102	3	1199	0	iPad Pro 11-inch - 256GB storage, A12Z Bionic chip
3200	3201	7	899	1	Microsoft Surface Pro 7 - 128GB storage, Intel Core i5 processor
3200	3202	2	1099	0	Microsoft Surface Pro 7 - 256GB storage, Intel Core i7 processor
3300	3301	5	1200	1	Lenovo ThinkPad X1 Carbon - 8GB RAM, 14-inch display, Intel Core i5 processor
3300	3302	3	1400	0	Lenovo ThinkPad X1 Carbon - 16GB RAM, 14-inch display, Intel Core i7 processor
3400	3401	4	1500	1	ASUS ROG Zephyrus G14 - 16GB RAM, 14-inch display, AMD Ryzen 9 processor
3400	3402	2	1700	0	ASUS ROG Zephyrus G14 - 32GB RAM, 14-inch display, AMD Ryzen 9 processor
3500	3501	10	299	1	Bose QuietComfort 35 II - Black, Wireless noise-cancelling headphones
3500	3502	5	349	0	Bose QuietComfort 35 II - Silver, Wireless noise-cancelling headphones
3600	3601	8	349	1	Sony WH-1000XM4 - Black, Wireless noise-cancelling headphones
3600	3602	4	399	0	Sony WH-1000XM4 - Silver, Wireless noise-cancelling headphones
3700	3701	15	149	1	JBL Charge 4 - Black, Portable Bluetooth speaker
3700	3702	10	169	0	JBL Charge 4 - Blue, Portable Bluetooth speaker
3800	3801	20	49	1	Amazon Echo Dot (4th Gen) - Charcoal, Smart speaker with Alexa
3800	3802	15	59	0	Amazon Echo Dot (4th Gen) - Glacier White, Smart speaker with Alexa
3900	3901	12	229	1	Google Nest Hub Max - Charcoal, Smart display with Google Assistant
3900	3902	8	249	0	Google Nest Hub Max - Chalk, Smart display with Google Assistant
4000	4001	25	149	1	Fitbit Charge 4 - Black, Fitness tracker with built-in GPS
4000	4002	20	169	0	Fitbit Charge 4 - Rosewood, Fitness tracker with built-in GPS
4100	4101	18	299	1	Garmin Forerunner 245 - Black, GPS running watch
4100	4102	12	329	0	Garmin Forerunner 245 - Aqua, GPS running watch
4200	4201	10	299	1	Oculus Quest 2 - 64GB, All-in-one VR headset
4200	4202	5	399	0	Oculus Quest 2 - 256GB, All-in-one VR headset
4300	4301	7	799	1	DJI Mavic Air 2 - Fly More Combo, Compact drone with 4K camera
4300	4302	3	999	0	DJI Mavic Air 2 - Standard, Compact drone with 4K camera
4400	4401	12	499	1	PlayStation 5 - Digital Edition, Next-gen gaming console
4400	4402	8	599	0	PlayStation 5 - Standard Edition, Next-gen gaming console
4500	4501	10	499	1	Xbox Series X - 1TB, Powerful gaming console
4500	4502	5	599	0	Xbox Series X - 2TB, Powerful gaming console
4600	4601	6	2999	1	Samsung QLED 8K TV - 65-inch, 8K resolution, Quantum Processor 8K
4600	4602	3	3999	0	Samsung QLED 8K TV - 75-inch, 8K resolution, Quantum Processor 8K
4700	4701	20	49	1	Roku Streaming Stick+ - Standard, 4K streaming device
4700	4702	10	59	0	Roku Streaming Stick+ - 4K, 4K streaming device
4800	4801	25	129	1	Kindle Paperwhite - 8GB, E-reader with high-resolution display
4800	4802	15	149	0	Kindle Paperwhite - 32GB, E-reader with high-resolution display
4900	4901	30	49	1	Philips Hue White and Color Ambiance - Single, Smart light bulb
4900	4902	20	89	0	Philips Hue White and Color Ambiance - 2-Pack, Smart light bulb
5000	5001	12	199	1	Ring Video Doorbell 3 - Standard, Smart doorbell with 1080p HD video
5000	5002	8	249	0	Ring Video Doorbell 3 - Plus, Smart doorbell with 1080p HD video
5100	5101	10	249	1	Nest Learning Thermostat - 3rd Gen, Smart thermostat with auto-schedule
5100	5102	5	299	0	Nest Learning Thermostat - 4th Gen, Smart thermostat with auto-schedule
5200	5201	20	29	1	TP-Link Kasa Smart Plug - Single, Wi-Fi smart plug with voice control
5200	5202	10	49	0	TP-Link Kasa Smart Plug - 2-Pack, Wi-Fi smart plug with voice control
5300	5301	15	199	1	August Smart Lock Pro - Silver, Smart lock with remote access
5300	5302	8	249	0	August Smart Lock Pro - Black, Smart lock with remote access
5400	5401	12	299	1	Arlo Pro 3 - Single Camera, Wireless security camera with 2K HDR video
5400	5402	6	499	0	Arlo Pro 3 - 2-Camera Kit, Wireless security camera with 2K HDR video
5500	5501	20	49	1	First Alert Smoke and CO Detector - Battery, Smart smoke and carbon monoxide detector
5500	5502	10	69	0	First Alert Smoke and CO Detector - Hardwired, Smart smoke and carbon monoxide detector
5600	5601	25	199	1	Sonos One - Black, Smart speaker with voice control
5600	5602	15	229	0	Sonos One - White, Smart speaker with voice control
5700	5701	30	79	1	Lenovo Smart Clock - Standard, Smart clock with Google Assistant
5700	5702	20	99	0	Lenovo Smart Clock - Essential, Smart clock with Google Assistant
5800	5801	10	299	1	Ray-Ban Stories - Wayfarer, Smart glasses with built-in cameras
5800	5802	5	349	0	Ray-Ban Stories - Round, Smart glasses with built-in cameras
5900	5901	12	399	1	GoPro HERO9 Black - Standard, Action camera with 5K video
5900	5902	8	449	0	GoPro HERO9 Black - Bundle, Action camera with 5K video
6000	6001	15	129	1	Garmin Dash Cam Mini - Standard, Compact dash camera with 1080p HD video
6000	6002	10	149	0	Garmin Dash Cam Mini - Bundle, Compact dash camera with 1080p HD video
6100	6101	20	199	1	Motorola MBP36XL - Standard, Video baby monitor with 5-inch screen
6100	6102	10	249	0	Motorola MBP36XL - Deluxe, Video baby monitor with 5-inch screen
6200	6201	15	199	1	Furbo Dog Camera - Standard, Pet camera with treat tossing
6200	6202	8	249	0	Furbo Dog Camera - Plus, Pet camera with treat tossing
6300	6301	25	29	1	Tile Pro - Black, High-performance Bluetooth tracker
6300	6302	15	39	0	Tile Pro - White, High-performance Bluetooth tracker
6400	6401	30	19	1	Anker PowerDrive 2 - Black, Dual USB car charger
6400	6402	20	29	0	Anker PowerDrive 2 - White, Dual USB car charger
6500	6501	20	29	1	iOttie Easy One Touch 4 - Standard, Car mount with one-touch locking mechanism
6500	6502	10	39	0	iOttie Easy One Touch 4 - Deluxe, Car mount with one-touch locking mechanism
6600	6601	15	299	1	Pioneer AVH-2500NEX - Standard, In-dash car stereo with 7-inch touchscreen
6600	6602	8	349	0	Pioneer AVH-2500NEX - Premium, In-dash car stereo with 7-inch touchscreen
6700	6701	20	79	1	Seagate Backup Plus Portable - 1TB, External hard drive
6700	6702	10	99	0	Seagate Backup Plus Portable - 2TB, External hard drive
6800	6801	25	49	1	SanDisk Extreme Pro SDXC - 64GB, High-performance memory card
6800	6802	15	79	0	SanDisk Extreme Pro SDXC - 128GB, High-performance memory card
6900	6901	30	19	1	Kingston DataTraveler 100 G3 - 32GB, USB flash drive
6900	6902	20	29	0	Kingston DataTraveler 100 G3 - 64GB, USB flash drive
7000	7001	15	199	1	TP-Link Archer AX6000 - Standard, High-speed Wi-Fi 6 router
7000	7002	8	249	0	TP-Link Archer AX6000 - Pro, High-speed Wi-Fi 6 router
7100	7101	20	179	1	Netgear Nighthawk X6S - Standard, Tri-band Wi-Fi router
7100	7102	10	229	0	Netgear Nighthawk X6S - Pro, Tri-band Wi-Fi router
7200	7201	12	299	1	Epson EcoTank ET-4760 - Standard, All-in-one printer with cartridge-free printing
7200	7202	6	349	0	Epson EcoTank ET-4760 - Deluxe, All-in-one printer with cartridge-free printing
7300	7301	15	129	1	Brother HL-L2350DW - Standard, Compact monochrome laser printer
7300	7302	8	149	0	Brother HL-L2350DW - Pro, Compact monochrome laser printer
7400	7401	10	99	1	Canon CanoScan LiDE400 - Standard, High-resolution flatbed scanner
7400	7402	5	129	0	Canon CanoScan LiDE400 - Premium, High-resolution flatbed scanner
7500	7501	20	79	1	Logitech C920s Pro HD Webcam - Standard, Full HD webcam with 1080p video
7500	7502	10	99	0	Logitech C920s Pro HD Webcam - Deluxe
"""
    sources['products_has_options'].append_to_file(generated_data)

def generate_users_and_user_has_creditcard(rows: int):
    last_user_id = sources['users'].read_last_line().split('\t')[0]
    
    generated_data_user = []
    generated_data_user_creditcard = []
    for i in range(rows):
        user_id = str(int(last_user_id)+1+i)
        profile = fake.simple_profile()
        username = profile['username']
        password = fake.password(6, False, True, False, True)
        full_name = profile['name']
        address = str(profile['address']).replace('\n',' ')
        email = profile['mail']
        phone = fake.phone_number()
        credit_card_number = fake.credit_card_number()
        generated_row_user = "\t".join([user_id, username, password, full_name, address, email, phone])
        generated_row_user_creditcard = "\t".join([user_id, credit_card_number])
        generated_data_user.append(generated_row_user)
        generated_data_user_creditcard.append(generated_row_user_creditcard)


    generated_data_user = "\n".join(sorted(generated_data_user))
    generated_data_user_creditcard = "\n".join(sorted(generated_data_user_creditcard))

    sources['users'].append_to_file(generated_data_user)
    sources['user_has_creditcards'].append_to_file(generated_data_user_creditcard)

def generate_orders_and_orders_has_product(rows: int):
    last_order_id = sources['orders'].read_last_line().split('\t')[0]
    
    product_ids = sources['products'].fetch_distinct_columns_values(0)
    option_ids = sources['options'].fetch_distinct_columns_values(0)

    option_ids = [x for x in option_ids if x[:2] in [x[:2] for x in product_ids]]
    order_dates = sorted([
        datetime(2018, 10, 21) + timedelta(rd.randint(1,60))
        for i in range(rows)
    ])
    chars = string.ascii_uppercase
    products_options = sources['products_has_options'].fetch_data()
    price_catalogue = {
        option_id_: price_ for option_id_, price_ in
        zip(
        [x['option_id'] for x in products_options],
        [x['price'] for x in products_options]
        )
    }

    generated_data_order = []
    generated_data_order_product = []

    for i in range(rows):
        order_id = str(int(last_order_id) + 1 + i)
        shipping_fee = str(rd.randint(1,20))
        tax = str(round(rd.randint(600, 1035) / 1000, 4))
        order_date = str(order_dates[i].date())
        delivery_date = str((order_dates[i] + timedelta(rd.randint(1,7))).date())
        ship_name = fake.name()
        ship_address = fake.address()
        tracking_number = ''.join([rd.choice(chars), rd.choice(chars), str(rd.randint(1001,9999))])
        delivery_status = rd.choice(['1','0'])
        item_distinct = rd.randint(1, 3)
        
        costs = []
        quantities = []
        for j in range(item_distinct):
            product_id = str(rd.choice(product_ids))
            option_id = str(rd.choice([x for x in option_ids if x[:2] == product_id[:2]]))
            price = int(price_catalogue[option_id])
            quantity = rd.randint(1, 23)
            cost = price * quantity
            quantities.append(quantity)
            costs.append(cost)
            generated_row_order_product = "\t".join([order_id, product_id, option_id, str(quantity)])
            generated_data_order_product.append(generated_row_order_product)
        
        total_item = str(sum(quantities))
        total_cost = str(sum(costs)+float(shipping_fee)+float(tax)*sum(costs)+rd.choice([10,15,20,25,30,35]))
        generated_row_order = "\t".join([order_id, total_item, shipping_fee, tax, total_cost, order_date, delivery_date, ship_name, ship_address, tracking_number, delivery_status])
        generated_data_order.append(generated_row_order)
  
    generated_data_order_product = "\n".join(sorted(generated_data_order_product))
    # sources['orders_has_products'].append_to_file(generated_data_order_product)
    generated_data_order = "\n".join(sorted(generated_data_order))
    # sources['orders'].append_to_file(generated_data_order)
    print(generated_data_order)
    print(generated_data_order_product)

generate_orders_and_orders_has_product(5)
# if __name__ == "__main__":
#     file_name = 'hello.txt'
#     text = 'Hello, world!'
#     append_to_file(file_name, text)
#     print(f"Appended '{text}' to {file_name}")
