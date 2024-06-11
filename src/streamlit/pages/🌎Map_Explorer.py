import streamlit as st
from datetime import date, date
import time
from gquery import *
from credentials import *
import pandas as pd
paesi_coordinate = {
    "Andorra": [42.5075, 1.5218],
    "Emirati Arabi Uniti": [23.4241, 53.8478],
    "Afghanistan": [33.9391, 67.7099],
    "Antigua e Barbuda": [17.0608, -61.7964],
    "Anguilla": [18.2206, -63.0686],
    "Albania": [41.1533, 20.1683],
    "Armenia": [40.0691, 45.0382],
    "Angola": [-11.2027, 17.8739],
    "Antartide": [-82.8628, -135.0000],
    "Argentina": [-38.4161, -63.6167],
    "Samoa Americane": [-14.2710, -170.1322],
    "Austria": [47.5162, 14.5501],
    "Australia": [-25.2744, 133.7751],
    "Aruba": [12.5211, -69.9683],
    "Isole Åland": [60.1785, 19.9156],
    "Azerbaigian": [40.1431, 47.5769],
    "Bosnia ed Erzegovina": [43.9159, 17.6791],
    "Barbados": [13.1939, -59.5432],
    "Bangladesh": [23.6850, 90.3563],
    "Belgio": [50.5039, 4.4699],
    "Burkina Faso": [12.2383, -1.5616],
    "Bulgaria": [42.7339, 25.4858],
    "Bahrain": [25.9305, 50.6374],
    "Burundi": [-3.3731, 29.9189],
    "Benin": [9.3077, 2.3159],
    "Saint-Barthélemy": [18.0956, -62.8481],
    "Bermuda": [32.3078, -64.7505],
    "Brunei": [4.5353, 114.7277],
    "Bolivia": [-16.2902, -63.5887],
    "Caribus Olandesi": [12.1784, -68.2385],
    "Brasile": [-14.2350, -51.9253],
    "Bahamas": [25.0343, -77.3963],
    "Bhutan": [27.5142, 90.4336],
    "Isola Bouvet": [-54.4208, 3.3492],
    "Botswana": [-22.3285, 24.6849],
    "Bielorussia": [53.7098, 27.9534],
    "Belize": [17.1899, -88.4976],
    "Canada": [56.1304, -106.3468],
    "Isole Cocos (Keeling)": [-12.1648, 96.8338],
    "Repubblica Democratica del Congo": [-4.0383, 21.7587],
    "Repubblica Centrafricana": [6.6111, 20.9394],
    "Repubblica del Congo": [-0.2281, 15.8277],
    "Svizzera": [46.8182, 8.2275],
    "Costa d'Avorio": [7.5400, -5.5471],
    "Isole Cook": [-21.2367, -159.7658],
    "Cile": [-35.6751, -71.5430],
    "Camerun": [3.8480, 11.5021],
    "Cina": [35.8617, 104.1954],
    "Colombia": [4.5709, -74.2973],
    "Costa Rica": [9.7489, -83.7534],
    "Cuba": [21.5218, -77.7812],
    "Capo Verde": [16.0000, -24.0000],
    "Curaçao": [12.1696, -68.9900],
    "Isola di Christmas": [-10.4475, 105.6904],
    "Cipro": [35.1264, 33.4299],
    "Repubblica Ceca": [49.8175, 15.4730],
    "Germania": [51.1657, 10.4515],
    "Gibuti": [11.8251, 42.5903],
    "Danimarca": [56.2639, 9.5018],
    "Dominica": [15.4150, -61.3710],
    "Repubblica Dominicana": [18.7357, -70.1627],
    "Algeria": [28.0339, 1.6596],
    "Ecuador": [-1.8312, -78.1834],
    "Estonia": [58.5953, 25.0136],
    "Egitto": [26.8206, 30.8025],
    "Sahara Occidentale": [24.2155, -12.8858],
    "Eritrea": [15.1794, 39.7823],
    "Spagna": [40.4637, -3.7492],
    "Etiopia": [9.1450, 40.4897],
    "Finlandia": [61.9241, 25.7482],
    "Figi": [-16.5783, 179.4167],
    "Isole Falkland": [-51.7963, -59.5236],
    "Stati Federati di Micronesia": [6.8874, 158.2155],
    "Isole Faroe": [61.8926, -6.9118],
    "Francia": [46.2276, 2.2137],
    "Gabon": [-0.8037, 11.6094],
    "Regno Unito": [55.3781, -3.4360],
    "Grenada": [12.2628, -61.6041],
    "Georgia": [42.3154, 43.3569],
    "Guyana Francese": [3.9339, -53.1258],
    "Guernsey": [49.5653, -2.5629],
    "Ghana": [7.9465, -1.0232],
    "Gibilterra": [36.1408, -5.3536],
    "Groenlandia": [71.7069, -42.6043],
    "Gambia": [13.4432, -15.3101],
    "Guinea": [9.9456, -9.6966],
    "Guadeloupe": [16.2671, -61.5518],
    "Guinea Equatoriale": [1.6508, 10.2679],
    "Grecia": [39.0742, 21.8243],
    "Georgia del Sud e Isole Sandwich Meridionali": [-54.4284, -37.0465],
    "Guatemala": [15.7835, -90.2308],
    "Guam": [13.4443, 144.7937],
    "Guinea-Bissau": [11.8037, -15.1804],
    "Guyana": [4.8604, -58.9302],
    "Hong Kong": [22.3193, 114.1694],
    "Isole Heard e McDonald": [-53.0800, 73.5167],
    "Honduras": [15.2000, -86.2419],
    "Croazia": [45.1000, 15.2000],
    "Haiti": [18.9712, -72.2852],
    "Ungheria": [47.1625, 19.5033],
    "Indonesia": [-0.7893, 113.9213],
    "Irlanda": [53.1424, -7.6921],
    "Israele": [31.0461, 34.8516],
"Isola di Man": [54.2361, -4.5481],
"India": [20.5937, 78.9629],
"Iraq": [33.2232, 43.6793],
"Iran": [32.4279, 53.6880],
"Islanda": [64.9631, -19.0208],
"Italia": [41.8719, 12.5674],
"Jersey": [49.2145, -2.1382],
"Giamaica": [18.1096, -77.2975],
"Giordania": [30.5852, 36.2384],
"Giappone": [36.2048, 138.2529],
"Kenya": [0.1864, 37.9063],
"Kirghizistan": [41.2044, 74.7661],
"Cambogia": [12.5657, 104.9910],
"Kiribati": [0.1725, 173.0274],
"Comore": [-11.6455, 43.3333],
"Saint Kitts e Nevis": [17.3578, -62.7830],
"Corea del Nord": [40.3399, 127.5101],
"Corea del Sud": [35.9078, 127.7669],
"Kuwait": [29.3117, 47.4818],
"Isole Cayman": [19.5150, -80.5668],
"Kazakistan": [48.0196, 66.9237],
"Laos": [19.8563, 102.4955],
"Libano": [33.8547, 35.8623],
"Santa Lucia": [13.9094, -60.9789],
"Liechtenstein": [47.1660, 9.5554],
"Sri Lanka": [7.8731, 80.7718],
"Liberia": [6.4281, -9.4295],
"Lesotho": [-29.6103, 28.2336],
"Lituania": [55.1694, 23.8813],
"Lussemburgo": [49.8153, 6.1296],
"Lettonia": [56.8796, 24.6032],
"Libia": [26.3351, 17.2283],
"Marocco": [31.7917, -7.0926],
"Monaco": [43.7384, 7.4246],
"Moldavia": [47.4116, 28.3699],
"Montenegro": [42.7087, 19.3744],
"Saint Martin": [18.0735, -63.0501],
"Madagascar": [-18.7669, 46.8691],
"Isole Marshall": [7.1315, 171.1845],
"Macedonia del Nord": [41.6086, 21.7453],
"Mali": [17.5703, -3.9962],
"Myanmar": [21.9162, 95.9560],
"Mongolia": [46.8625, 103.8467],
"Macao": [22.1987, 113.5439],
"Isole Marianne Settentrionali": [15.0979, 145.6739],
"Martinica": [14.6603, -61.0241],
"Mauritania": [21.0079, -10.9408],
"Monserrat": [16.7420, -62.1874],
"Malta": [35.9375, 14.3754],
"Mauritius": [-20.3484, 57.5522],
"Maldive": [3.2028, 73.2207],
"Malawi": [-13.2543, 34.3015],
"Messico": [23.6345, -102.5528],
"Malaysia": [4.2105, 101.9758],
"Mozambico": [-18.6657, 35.5296],
"Namibia": [-22.9576, 18.4904],
"Nuova Caledonia": [-20.9043, 165.6180],
"Niger": [17.6078, 8.0817],
"Isola Norfolk": [-29.0546, 167.9547],
"Nigeria": [9.0820, 8.6753],
"Nicaragua": [12.8654, -85.2072],
"Paesi Bassi": [52.1326, 5.2913],
"Norvegia": [60.4720, 8.4689],
"Nepal": [28.3949, 84.1240],
"Nauru": [-0.5228, 166.9325],
"Niue": [-19.0544, -169.8672],
"Nuova Zelanda": [-40.9006, 174.8860],
"Oman": [21.5121, 55.9231],
"Panama": [8.5380, -80.7821],
"Perù": [-9.1900, -75.0152],
"Polinesia Francese": [-17.6797, -149.4068],
"Papua Nuova Guinea": [-6.3150, 143.9555],
"Filippine": [12.8797, 121.7741],
"Pakistan": [30.3753, 69.3451],
"Polonia": [51.9194, 19.1451],
"Saint-Pierre e Miquelon": [46.9420, -56.2708],
"Isole Pitcairn": [-24.7033, -127.4392],
"Porto Rico": [18.2208, -66.5901],
"Palestina": [31.9522, 35.2332],
"Portogallo": [39.3999, -8.2245],
"Palau": [7.5150, 134.5825],
"Paraguay": [-23.4425, -58.4438],
"Qatar": [25.3548, 51.1839],
"Riunione": [-21.1351, 55.2471],
"Romania": [45.9432, 24.9668],
"Serbia": [44.0165, 21.0059],
"Russia": [61.5240, 105.3188],
"Ruanda": [-1.9403, 29.8739],
"Arabia Saudita": [23.8859, 45.0792],
"Isole Salomone": [-9.6457, 160.1562],
"Seychelles": [-4.6796, 55.4920],
"Sudan": [12.8628, 30.2176],
"Svezia": [60.1282, 18.6435],
"Singapore": [1.3521, 103.8198],
"Sant'Elena": [-15.9670, -5.7093],
"Slovenia": [46.1512, 14.9955],
"Svalbard e Jan Mayen": [77.5522, 23.6707],
"Slovacchia": [48.6690, 19.6990],
"Sierra Leone": [8.4605, -11.7799],
"San Marino": [43.9424, 12.4578],
"Senegal": [14.4974, -14.4524],
"Somalia": [5.1521, 46.1996],
"Suriname": [3.9193, -56.0278],
"Sao Tome e Principe": [0.1864, 6.6131],
"El Salvador": [13.7942, -88.8965],
"Sint Maarten": [18.0425, -63.0548],
"Siria": [34.8021, 38.9968],
"Eswatini": [-26.5225, 31.4659],
"Isole Turks e Caicos": [21.6942, -71.7979],
"Ciad": [15.4542, 18.7322],
"Territori Francesi del Sud": [-49.2806, 69.3477],
"Togo": [8.6195, 0.8248],
"Thailandia": [15.8700, 100.9925],
"Tagikistan": [38.8610, 71.2760],
"Tokelau": [-8.9675, -171.8505],
"Timor Est": [-8.8742, 125.7275],
"Turkmenistan": [38.9697, 59.5563],
"Tunisia": [33.8869, 9.5375],
"Tonga": [-21.1789, -175.1982],
"Turchia": [38.9637, 35.2433],
"Trinidad e Tobago": [10.6918, -61.2225],
"Tuvalu": [-7.1095, 177.6493],
"Taiwan": [23.6978, 120.9605],
"Tanzania": [-6.3690, 34.8888],
"Ucraina": [48.3794, 31.1656],
"Uganda": [1.3733, 32.2903],
"Isole Minori Lontane degli Stati Uniti": [19.2823, 166.6470],
"Stati Uniti": [37.0902, -95.7129],
"USA":[37.0902, -95.7129],
"Uruguay": [-32.5228, -55.7658],
"Uzbekistan": [41.3775, 64.5853],
"Città del Vaticano": [41.9029, 12.4534],
"Saint Vincent e Grenadine": [12.9843, -61.2872],
"Venezuela": [6.4238, -66.5897],
"Isole Vergini Britanniche": [18.4207, -64.6400],
"Isole Vergini Americane": [18.3358, -64.8963],
"Vietnam": [14.0583, 108.2772],
"Vanuatu": [-15.3767, 166.9592],
"Wallis e Futuna": [-13.7686, -177.1762],
"Samoa": [-13.7590, -172.1046],
"Yemen": [15.5527, 48.5164],
"Mayotte": [-12.8275, 45.1662],
"Sudafrica": [-30.5595, 22.9375],
"Zambia": [-13.1339, 27.8493],
"Zimbabwe": [-19.0154, 29.1549],
"Serbia": [44.0165, 21.0059]
}


def main():
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))
    st.header("""Map Explorer :earth_africa:""", divider='blue')
    st.markdown("""Il Map Explorer consente di filtrare per mese di pubblicazione degli articoli e visualizzare i Paesi menzionati su una mappa mondiale 
              con pallini colorati diversamente in base al numero di connessioni. La mappa è accompagnata da un grafico a barre che mostra
               il numero di connessioni per ciascun Paese selezionato, insieme a una rappresentazione tabellare dettagliata dei Paesi e delle connessioni""")
    start_date = date(2022, 9, 1)
    end_date = date.today()

    # Slider per selezionare la data
    selected_date = st.slider('Seleziona mese e anno', min_value=start_date, max_value=end_date, value=date(2023, 10, 1), format="MMM YYYY")

    # Estrai anno e mese dalla data selezionata
    selected_year = selected_date.year
    selected_month = selected_date.month



    with driver.session() as session:
        luoghi_connessi = get_luoghi_mese_anno(driver, selected_year, selected_month)
    #driver.close()
    # Prepara i dati per la mappa e il DataFrame finale
    data=[]
    for nodo in luoghi_connessi:
        nome = nodo[0]
        connessioni = nodo[1]
        if connessioni > 6:
            colore = "#ff0055"
            dim=10
        elif connessioni>3 and connessioni <=6:
            colore = "#ff7300"
            dim=7
        else:
            colore = "#030bff"
            dim=5
        if nome in paesi_coordinate:
            lat, lon = paesi_coordinate[nome]
            data.append({"latitude": lat, "longitude": lon, "nome": nome, "connessioni": connessioni, "colore": colore,"dimensione": dim})


    
    df_map = pd.DataFrame(data)
    st.map(df_map, color="colore",size="dimensione",zoom=0.85)


    df_connessioni = pd.DataFrame([(istanza["nome"], istanza["connessioni"]) for istanza in data], columns=["Nome", "Numero_connessioni"])
    col1,col2=st.columns([0.65,0.35])
    with col1:
        st.bar_chart(df_map,x="nome",y="connessioni", use_container_width=True, color="#6697f2")
    with col2:
        st.write(df_connessioni)
if __name__ == "__main__":
    main()