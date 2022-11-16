
import requests
import json
import time
from configparser import ConfigParser 

config = ConfigParser() 
config.read('config.ini')

def webexCreateMessage(message):
    '''
    Description
    '''
    # webex bot create message in room (messages from location ISS)
    HTTPHeaders = { 
          "Authorization": AccessTokenWebex,
          "Content-Type": "application/json"
    }
    PostData = {
          "roomId": roomIdToGetMessages,
          "text": message
    }
    r = requests.post(config.get('WEBEX', 'webexUrlMessagesPost'), 
                          data = json.dumps(PostData), 
                              headers = HTTPHeaders
    )



##############     CHFPTER 1      ##############
# Webex Authentication 

AccessTokenWebex = config.get('WEBEX', 'AccessTokenWebex')

print ('Use Default Webex token')
choice = input("Enter new webex token (y/n) ")
if choice == "Y" or choice == "y":
    AccessTokenWebex = input("What is your access token?\n")
AccessTokenWebex = "Bearer " + AccessTokenWebex



##############     CHFPTER 2      ##############
# Webex show rooms
r = requests.get(   config.get('WEBEX', 'webexUrlRooms'),
                    headers = {"Authorization": AccessTokenWebex}
                )


if not r.status_code == 200:
    raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))


# Webex print rooms
print("\nList of Rooms:")
rooms = r.json()["items"]

for i in range(len(rooms)):
    print(i, '-', rooms[i]['title'])
else:
    print('Total rooms: ' + str(len(rooms)))


##############     CHFPTER 3     ##############
# Webex chose room 
while True:
    roomNumberToSearch = int(input("\nRoom number: ")) 

    if roomNumberToSearch >= 0 and roomNumberToSearch < len(rooms):
        roomIdToGetMessages = rooms[roomNumberToSearch]["id"]
        roomTitleToGetMessages = rooms[roomNumberToSearch]["title"]
        print("Select room : " + roomTitleToGetMessages)
        print("Id room : " + roomIdToGetMessages + '\n')
        break
    else:
        print("Sorry, I didn't find any room.")
        print("Please try again...")


##############     CHFPTER 4     ##############
# Webex bot (listen)
while True:
    time.sleep(1)
    GetParameters = {
                            "roomId": roomIdToGetMessages,
                            "max": 1 #max_message
                    }


                    
# Webex bot show messages
    r = requests.get(config.get('WEBEX', 'webexUrlMessages'), 
                         params = GetParameters, 
                         headers = {"Authorization": AccessTokenWebex}
                    )

    if not r.status_code == 200:
        raise Exception( "Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))
    
    json_data = r.json()
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")
    
    messages = json_data["items"]
    message = messages[0]["text"]
    print("Last message: " + message)
    
 # Webex bot found a match  
    if message.find("/Help") == 0:
        responseMessage = '*************************************\n' + '/ISS - show location ISS\n' + '/ISS_crew - show ISS crew\n' + '*************************************' 
        webexCreateMessage(responseMessage)

    
    elif message.find("/ISS_crew") == 0:
        # iss request (crew)
        r_iss_crew = requests.get(config.get('ISS', 'issUrlCrew'))
        r_iss_crew_json = r_iss_crew.json()['people']

        crew = ''
        for crew_numb in range(len(r_iss_crew_json)):
            crew = crew + r_iss_crew_json[crew_numb]['name'] + '\n'

        webexCreateMessage('How many humans are in space right now?')

        responseMessage = crew
        webexCreateMessage(responseMessage)
 

    elif message.find("/ISS") == 0:

        # iss request (location, coordinates)
        r_iss = requests.get(config.get('ISS', 'issUrl'))
        r_iss_json = r_iss.json()['iss_position']
        coordinates_iss = r_iss_json['latitude'] + ',' + r_iss_json['longitude']


        # MapQuest request (geocoding)
        AccessTokenWebexMapQuest = config.get('MAPQUEST', 'AccessTokenWebexMapQuest') 

        url = config.get('MAPQUEST', 'mapQuesUrl') 
        headers = {'Content-Type': 'application/json'}
        params = {'location': coordinates_iss, 'key': AccessTokenWebexMapQuest}

        res = requests.get(url, headers=headers, params=params)
        res_json = res.json()['results'][0]['locations'][0]

        print(json.dumps(res_json, indent=4))
        
        if res_json['adminArea1'] != '':
            webexCreateMessage('The ISS is moving at close to 28,000 km/h so its location changes really fast! Where is it right now?')

            responseMessage = '''
ISS coordinates:  {coordinates}
*************************************
Country:  {country}
City:  {city}
Street:  {street}
*************************************
'''.format(coordinates = coordinates_iss, country = res_json['adminArea1'], city = res_json['adminArea5'], street=res_json['street'])
            webexCreateMessage(responseMessage)
        else:
            responseMessage = 'The ISS is moving at close to 28,000 km/h so its location changes really fast! Where is it right now?'
            webexCreateMessage(responseMessage)

            responseMessage = '\nISS coordinates:  ' + coordinates_iss + '\n' + '*************************************\n' + 'ISS Location: Neutral Earth/Water\n' + '*************************************\n' 
            webexCreateMessage(responseMessage)

            












        



    


