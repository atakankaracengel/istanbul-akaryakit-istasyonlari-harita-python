import requests
import pandas as pd
import folium


all_data = pd.DataFrame()


offset = 0
limit = 100  
resource_id = "5625860c-d79a-446f-898e-2aa2b9099bc8"

while True:
    
    url = f"https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id={resource_id}&limit={limit}&offset={offset}"
    response = requests.get(url)
    data = response.json()
    
    
    df = pd.DataFrame(data['result']['records'])
    
    
    if df.empty:
        break
    
    
    all_data = pd.concat([all_data, df], ignore_index=True)
    
   
    offset += limit


all_data['latitude'] = pd.to_numeric(all_data['latitude'], errors='coerce')
all_data['longtitude'] = pd.to_numeric(all_data['longtitude'], errors='coerce')


all_data = all_data.dropna(subset=['latitude', 'longtitude'])


istanbul_center = [41.0082, 28.9784]  
mymap = folium.Map(location=istanbul_center, zoom_start=10)


total_stations = len(all_data)
title_html = f'''
             <h3 align="center" style="font-size:20px"><b>Toplam Akaryakıt İstasyonu Sayısı: {total_stations}</b></h3>
             '''
mymap.get_root().html.add_child(folium.Element(title_html))


for _, row in all_data.iterrows():
    folium.Marker(
        location=[row['longtitude'], row['latitude']],
        popup=f"İlçe: {row['ilce']}\nMahalle: {row['mahalle_adi']}\nTesis: {row['is_nevi_tnm']}",
        icon=folium.Icon(color="blue")
    ).add_to(mymap)


mymap.save("istanbul_akaryakit_istasyonlari.html")

mymap
