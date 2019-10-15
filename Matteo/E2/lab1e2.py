import json
import os
folderPath = os.getcwd()
slash='/'


from math import cos, acos, sin
def distance_coords(lat1, lng1, lat2, lng2): 
    """Compute the distance among two points.""" 
    deg2rad = lambda x: x * 3.141592 / 180 
    lat1, lng1, lat2, lng2 = map(deg2rad, [ lat1, lng1, lat2, lng2 ]) 
    R = 6378100 # Radius of the Earth, in meters 
    return R * acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lng1 - lng2))

with open(folderPath + slash + 'citybik.json') as f: 
    obj = json.load(f)
    
stationsList = obj['network']['stations']

#2. Countandprintthenumberofactivestations(astationisactiveifitsextra.statusﬁeldis"online"). 
print('2.')
print('\tNumber of active stations:' + str(len(list(filter(lambda str: str['extra']['status']=='online',stationsList)))))

#3. Countandprintthetotalnumberofbikesavailable(ﬁeldfree_bikes)andthenumberoffreedocks (ﬁeld empty_slots) throughout all stations. 
print('3.')
print('\tBikes available:' + str(sum(map(lambda x: int(x['free_bikes']) ,stationsList))))
print('\tFree docks:' + str(sum(map(lambda x: int(x['empty_slots']) ,stationsList))))

#4. (*) Given the coordinates (latitude, longitude) of a point (e.g. 45.074512,7.694419), identify the closest bike station to it that has available bikes. For computing the distance among two points (giventheircoordinates),youcanusethefunction distance_coords() deﬁnedinthecodesnippet below (which is an implementation of the great-circle distance):
print('4.')
my_lat=45.09878
my_long=7.624568

#distanceMap is a dictionary having the name station as key and distance as value
distanceMap=list(map(lambda x: [x['name'],distance_coords(my_lat,my_long,x['latitude'],x['longitude'])],stationsList))
station,distance=min(distanceMap,key = lambda x:x[1])
print(f'\tClosest station is {station} at a distance of {distance} meters')
        

    








    