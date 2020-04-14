
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from distutils.dir_util import copy_tree
import time
import os
from pyvirtualdisplay import Display

start_time = time.time()
print ('Starting Script...')

#Uncomment to run without opening Chrome (headless) (~55 Second Runtime)
#Commented = ~60 second runtime
display = Display(visible=0, size=(1200, 800))
display.start()
 
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.default_directory": r"/home/pi/Desktop/PortablePhotos",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

#Address of USB Stick folder: /media/pi/23A4-6147/PortablePhotos
#Gave crdownload partial file error. Gave 6-8 extra photos. 
#Downloading to Pi then copying to USB gets rid of that error. 

#Open up Chrome Webdriver
driver = webdriver.Chrome(chrome_options=options)
print ('Loading Chrome')
driver.implicitly_wait(10) #waits for element to be found for all code


#Load camera website 
driver.get('http://192.168.1.43/login')
driver.set_window_size(720, 720)
print ('Webpage loaded')

#Log into the camera
username = driver.find_element_by_name("user_name").send_keys('admin')
password = driver.find_element_by_name("user_password").send_keys("admin")
login = driver.find_element_by_id("button-login").click()
print ('Logged in')

#Access Storage page of photos 
storagePage = driver.find_element_by_link_text('STORAGE').click()
print ('Storage Page Accessed')

#Start Downloading photos
driver.implicitly_wait(10)
links = driver.find_elements_by_css_selector('.button.button-storage-save')

#Loop to iterate through all links and click (download) them
for i in links:
    i.click()

time.sleep(1)
print ('Photos Downloaded, Chrome Closed')
driver.close()
print('Transferring Photos to USB')
copy_tree("/home/pi/Desktop/PortablePhotos", "/media/pi/23A4-6147/PortablePhotos")
print('Photos Transferred to USB')

print ('Checking for Duplicates')

#Removes all Duplicate Photos
#USB
file_path = r"/media/pi/23A4-6147/PortablePhotos"

#Pi
file_path2 = r"/home/pi/Desktop/PortablePhotos"

file_list = os.listdir(file_path)
file_list2 = os.listdir(file_path2)

for file_name in file_list:
    if " (1)" not in file_name:
        continue
    original_file_name = file_name.replace(' (1)', '')
    if not os.path.exists(os.path.join(file_path, original_file_name)):
        continue  # do not remove files which have no original
    os.remove(os.path.join(file_path, file_name))
    
for file_name in file_list2:
    if " (1)" not in file_name:
        continue
    original_file_name = file_name.replace(' (1)', '')
    if not os.path.exists(os.path.join(file_path2, original_file_name)):
        continue  # do not remove files which have no original
    os.remove(os.path.join(file_path2, file_name))

print ('Duplicates Deleted')

print('Program Done')

print ("--- %s seconds ---" % (time.time()- start_time))

#exit()
