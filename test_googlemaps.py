import googlemaps
from pygeocoder import Geocoder
from urllib import request

def download_pic(url,filename):
    img = request.urlopen(url)
    localfile = open( "./" + str(filename) + ".png" , 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()

# GoogleMaps API
gmaps = googlemaps.Client(key="AIzaSyBRRmlCHEWhI9m7WLOgGNuGtBT9sxfoSzc")
geocode_result = gmaps.geocode("東中野",language="ja")
print(geocode_result)
directions_result = gmaps.directions('戸塚駅','踊場駅',mode="driving",alternatives=False,language="ja")
#print(directions_result)

for a_idx in range(0, len(directions_result)):
    #print(directions_result[a_idx])
    a_legs = directions_result[a_idx]['legs']
    for a_idx_legs in range(0, len(a_legs)):
        print("********************" + str(a_idx_legs) + "********************\n")
        print(a_legs[a_idx_legs]['start_location'])
        #print("\n")
        print(a_legs[a_idx_legs]['end_location'])
        #print("\n")
        print(a_legs[a_idx_legs]['distance'])
        #print("\n")
        print(a_legs[a_idx_legs]['duration'])
        #print("\n")
        a_steps = a_legs[a_idx_legs]['steps']
        for a_idx_steps in range(0, len(a_steps)):
            print("********************" + str(a_idx_steps) + "********************\n")
            print(a_steps[a_idx_steps]['start_location'])
            #print("\n")
            print(a_steps[a_idx_steps]['end_location'])
            #print("\n")
            print(a_steps[a_idx_steps]['distance'])
            #print("\n")
            print(a_steps[a_idx_steps]['duration'])
            #print("\n")
            print(a_steps[a_idx_steps]['html_instructions'])
            #print("\n")
            print(a_steps[a_idx_steps]['polyline'])
            #print("\n")
            print(a_steps[a_idx_steps]['travel_mode'])
            #print("\n")

exit(0)

# Geocoder
address = "国会議事堂"
results = Geocoder.geocode(address)
print(results[0].coordinates)
result = Geocoder.reverse_geocode(*results.coordinates, language="ja")
print(result)

# GoogleMaps
address = '札幌駅'
#address = 'ホワイトハウス'
results = Geocoder.geocode(address)
print(results[0].coordinates)
result = Geocoder.reverse_geocode(*results.coordinates, language="ja")
print(result)
html1 = "https://maps.googleapis.com/maps/api/staticmap?center="
html2 = "&maptype=hybrid&size=640x480&sensor=false&zoom=18&markers="
html3 = ""
#html3 = "&key=AIzaSyBRRmlCHEWhI9m7WLOgGNuGtBT9sxfoSzc"
axis = str((results[0].coordinates)[0]) + "," + str((results[0].coordinates)[1])
html = html1 + axis + html2 + axis + html3
print(html)
download_pic(html,address)
