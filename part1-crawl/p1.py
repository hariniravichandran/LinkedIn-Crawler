import re
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.keys import Keys
import endorse_queue_file
import endorsements_file
import name_id_map_file
import traversal_order_file
import time
import unicodedata
driver = webdriver.Chrome()
driver.get('http://www.linkedin.com')
user_name= driver.find_element_by_id('login-email')
password= driver.find_element_by_id('login-password')
user_name.send_keys('your_userid')
password.send_keys('your_password')
submit = driver.find_element_by_xpath("//*[@type='submit']")
submit.submit()
endorsements = endorsements_file.endorsements
endorse_queue = endorse_queue_file.endorse_queue
traversal_order = traversal_order_file.traversal_order
name_id_map = name_id_map_file.name_id_map
anon_map = {}
limit = 1050
urlbase = "https://www.linkedin.com/profile/view?id="

def find_next(endorse_list):
    elem = endorse_list[0]
    endorse_list = endorse_list[1:]
    return elem, endorse_list

def form_url(id):
    url = urlbase + str(id)
    return url

def exceeds_limit(endorsements):
    if len(endorsements) > limit:
        return True
    return False

def get_name_from_id(profile_id):
    name = ''
    address = form_url(profile_id)
    time.sleep(30)
    driver.get(address)
    n = driver.find_element_by_xpath('//*[@id="name"]/h1/span/span').text
    name = unicodedata.normalize('NFKD', n).encode('ascii','ignore')
    #print "In get_name_from_id: ",profile_id, name
    return name

def get_endorsers(address):
    global endorse_queue
    global endorsements
    global name_id_map
    #print "In get_endorsers: "
    time.sleep(30)
    driver.get(address)
    key = address.split('=')[-1].split('/')[-1]
    n = driver.find_element_by_xpath('//*[@id="name"]/h1/span/span').text
    name = unicodedata.normalize('NFKD', n).encode('ascii','ignore')
    print type(name)
    source = driver.page_source
    modSource = source.split('facePileEndorserIds:')[-1]
    temp = re.search(r'([^a-zA-Z])*',modSource).group()
    temp = temp.replace('[','').replace(']','').encode('ascii','ignore')
    temp1 = temp.split(',')
    endorsement_list = filter(None, list(set(temp1)))
    endorsement_list = [val.strip() for val in endorsement_list]
    endorsement_list = [val for val in endorsement_list if val.isdigit()]
    endorse_queue.extend(endorsement_list)
    endorsements[key] = endorsement_list
    traversal_order.append(key)
    name_id_map[key] = name
    print "User count: ",len(endorsements), name, endorsement_list

def traverse_people(profile_id):
    global endorse_queue
    global endorsements
    print "In traverse_people: ",profile_id
    if exceeds_limit(endorsements): 
        return
    #print "After limit check: ", len(endorsements)
    address = form_url(profile_id)
    print "address: ", address
    get_endorsers(address)
    while endorse_queue:
        if len(endorsements) == limit: 
            break
        write_dicts()
        next_id, endorse_queue = find_next(endorse_queue)
        if next_id not in endorsements:
            #print "Calling traverse_people: ",len(endorsements)
            traverse_people(next_id)
    return

def write_to_file():
    global anon_map
    count = 1
    for key, val in endorsements.items():
        for id in val:
            if id not in name_id_map:
                #name = get_name_from_id(id)
                name_id_map[id] = id
    #print "name_id_map: ", name_id_map
    for key in traversal_order:
        csv3 = open('Csvs/anon_map.csv', 'a')
        csvwriter3 = csv.writer(csv3, delimiter = ',', quoting=csv.QUOTE_MINIMAL)
        csv4 = open('Csvs/anon_edge_list.csv', 'a')
        csvwriter4 = csv.writer(csv4, delimiter = ',', quoting=csv.QUOTE_MINIMAL)
        name = name_id_map[key]
        if name not in anon_map:
            anon_map[name] = count
            print "Writing anon_map 1: ", count
            csvwriter3.writerow([name, count])
            count += 1
        endorsers = [name_id_map[val] for val in endorsements[key]]
        with open('Csvs/edge_list.csv', 'a') as csvfile:
            csvwriter1 = csv.writer(csvfile, delimiter = ',', quoting=csv.QUOTE_MINIMAL)
            for endorser in endorsers:
                if endorser not in anon_map:
                    anon_map[endorser] = count
                    print "Writing anon_map 2: ", count
                    csvwriter3.writerow([endorser, count])
                    count += 1
                #print name, endorser
                csvwriter1.writerow([name, endorser])
                csvwriter4.writerow([anon_map[name], anon_map[endorser]])
        with open('Csvs/edge_count.csv', 'a') as csv2:
            csvwriter2 = csv.writer(csv2, delimiter = ',', quoting=csv.QUOTE_MINIMAL)
            print "Writing edge_count"
            csvwriter2.writerow([name, len(endorsements[key])])
        



def write_dicts():
    dicts_to_write = ['endorsements', 'name_id_map', 'traversal_order', 'endorse_queue', 'anon_map']
    for ds in dicts_to_write:
        print "Writing dict: ", ds
        f1 = open("Dicts/"+ds+".py", "w")
        f1.write(ds+"="+str(eval(ds)))
        f1.close()

start_id = '227767200'
print start_id
traverse_people(start_id)
write_to_file()
write_dicts()
print "Done"