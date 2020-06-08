import requests 
import json
import pandas as pd

# function to get a dataframe from the yelp api of restaurant data
def getRestaurantData(location):
    API_KEY= # use own API key here 
    ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
    HEADERS = {"Authorization": 'bearer %s' % API_KEY }

    location_list = location.split(",")
    for i in range(len(location_list)):
        location_list[i] = float(location_list[i])
    
    PARAMETERS = {'term': 'restaurant',
                  'latitude': location_list[0],
                  'longitude': location_list[1],
                  'limit': 50}
    # make API call
    response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)
    # Convert a response to a JSON string
    restaurant_data = response.json() 

    # save results for future use
    with open('restaurant.json', 'w') as json_file:
        json.dump(restaurant_data, json_file, indent = 3)

    # create a dataframe
    df = pd.DataFrame(restaurant_data['businesses'])
    return df

# function to clean the dataframe from the yelp api
def cleanDataframe(df): 

    ## creating columns for the latitudes and longitudes of restaurants returned
    latitudes = []
    longitudes = []
    coordinates = df['coordinates']
    for i in range(len(coordinates)):
        latitudes.append(coordinates[i]['latitude'])
        longitudes.append(coordinates[i]['longitude'])

    df['latitude'] = latitudes
    df['longitude'] = longitudes

    ##Fixing categories column
    categories = df['categories']
    descriptors = []
    for i in range(len(categories)):
        this_restaurant_descriptors = ""
        for entry in categories[i]:
            if (categories[i].index(entry) < (len(categories[i]) - 1)):
                this_restaurant_descriptors = this_restaurant_descriptors + entry['title'] + ", "
            else: 
                this_restaurant_descriptors = this_restaurant_descriptors + entry['title']
        descriptors.append(this_restaurant_descriptors)
    df["descriptors"] = descriptors

    #changing locations to the 'display address' field within the location list
    locations = df['location']
    addresses = []
    for i in range(len(locations)):
        display_address_list = locations[i]['display_address']
        string_address = ""
        for i in range(len(display_address_list)):
            string_address += display_address_list[i]
            if (i == 1 and (len(display_address_list) > 2)): 
                if (len(display_address_list[i]) != 0):
                    string_address += ", "
            string_address += " "
        addresses.append(string_address)
    df['address'] = addresses

    # Fix distance column
    # converting meters to miles 
    # numMiles = 0.00062137 * numMeters
    inmiles = []
    distance = df['distance']
    for i in range(len(distance)):
        new_distance = distance[i] * 0.00062137
        inmiles.append(new_distance)
    df['distance_in_miles'] = inmiles

    #Fix transactions column
    getfood = []
    reservation = []
    transactions = df['transactions']
    for i in range(len(transactions)):
        if 'restaurant_reservation' in transactions[i]:
            reservation.append(True)
        else:
            reservation.append(False)
        getfood_methods = ""
        for element in transactions[i]:
            if (element == 'delivery' or element == 'pickup'):
                getfood_methods += element.capitalize()
                if (transactions[i].index(element) == 0 and (len(transactions[i]) > 1)):
                    getfood_methods += ", "
        getfood.append(getfood_methods)
    df['getfood'] = getfood
    df['reservation'] = reservation


    #Deleted unnecessary columns

    #delete alias column because information is included in name column
    del df['alias']
    #delete categories column because information is included in the descriptors column
    del df['categories']
    #delete coordinates column because already pulled that information
    del df['coordinates']
    #delete phone column because info is already in better format in display_phone column
    del df['phone']
    #delete locations column because info has been pulled
    del df['location']
    #deleting old distance column
    del df['distance']
    #delete transactions column because info has been pulled
    del df['transactions']

    df = df.reindex(columns = ['name', 'descriptors', 'address', 'price', 'rating', 'review_count', 'is_closed','reservation', 'getfood', 'display_phone', 'distance_in_miles', 'latitude', 'longitude', 'image_url', 'id'])
    return df

    
## Testing above functions with a hard-coded location
# data = getRestaurantData("39.0438,-77.4874")
# newdata = cleanDataframe(data)
# print(newdata['address'])

