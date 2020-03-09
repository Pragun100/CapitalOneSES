from flask import Flask
from flask import render_template, make_response
from flask import redirect, request, jsonify, url_for
import folium 
from folium import Map, Marker, GeoJson, LayerControl
import requests
import json
from calculations import getRestaurantData, cleanDataframe
import geocoder 



app = Flask(__name__)

@app.route('/')
def getMap():

    # initialize the map to the starting location and add starting location
    # this library will base location off user IP address. It works locally, but 
    # not once the app is deployed (different IP address)
    g = geocoder.ip('me')
    start_coords = g.latlng
    themap = Map(location = start_coords,
             tiles = "OpenStreetMap",
             zoom_start = 15)
    folium.Marker(
        location=start_coords,
        popup='Your Location',
        icon=folium.Icon(color='red', icon = 'hi')).add_to(themap)
    
    
    # get nearby restaurant data 
    startloc = str(start_coords[0]) + "," + str(start_coords[1])
    df = getRestaurantData(startloc)
    data = cleanDataframe(df)
    
    # add restaurants to the map
    for (y,x) in data.iterrows():
        loc = []
        loc.append(x['latitude'])
        loc.append(x['longitude'])
        color = "green"
        if (x['rating'] < 4.0):
            color = "orange"
        popup_text = "{}<br> Cuisine: {}<br> Average Rating: {}<br> Number of Reviews: {}"
        popup_text = popup_text.format(x["name"],
                           x["descriptors"],
                           x["rating"],
                           x['review_count'])
        themap.add_child(Marker(location = loc, popup = popup_text, icon = folium.Icon(color = color)))
    return themap._repr_html_()


# this was an attempt to gather user location using the html5 api and AJAX module

# @app.route('/getlocation', methods = ['POST'])
# def getLocationData():
#     location_data = request.form['location']
#     return(json.dumps({'yourlocation': location_data}))
    

if __name__ == '__main__':
    app.run(debug = True)



