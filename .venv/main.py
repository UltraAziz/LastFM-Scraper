import json
from bs4 import BeautifulSoup
import requests


def get_config_data(parameter):  #Parameter is the setting to be extracted from the config.json file
    with open("config.json", "r") as read_file:
        config = json.load(read_file)  #Stores config.json in variable
        parameter = config[f"{parameter}"]

        return str(parameter)


# Process to get html data of last.fm profile page
URL = f"https://www.last.fm/user/{get_config_data("username")}"  #Profile URL
lastfm = requests.get(URL)  #Fetches data from website
soup = BeautifulSoup(lastfm.content, "html.parser")  #Converts data into proper html formatting


# End of process to get html data of last.fm profile page

#Process to get data from grids (artists and albums)
def get_grid_data(number_of_entries, index):
    counter = 0
    main_text_divs = [div for div in
                      soup.find_all('div',
                                    class_="grid-items-item-details")]  #A list of all div elements with this class
    initial_a_list = [div.find_all('a', class_="link-block-target") for div in
                      main_text_divs]  #All links within the div elements
    entry_list = []

    for a in initial_a_list:
        link = str(a)  #Stores the a element as a string
        split_link = link.split('"')  #Splits links at every quotation mark
        entry_list.append(split_link[5])  #Adds the artist name to the artist list
        # (Artist name has the index [5] after splitting the links
        counter += 1
        if counter == int(number_of_entries):
            break  #Stops the loop when it goes through all the artists

    aux_test_p = [p for p in soup.find_all('p', class_="grid-items-item-aux-text")]  #List of p elements with that class
    a_list = [p.find_all('a') for p in aux_test_p]  #Links within those p elements

    plays_list = []

    for a in a_list:
        link = str(a)
        link = link.replace('<', '>')  #For easier splitting
        split_link = link.split('>')

        if len(split_link) >= index:  #To avoid an index error
            number_of_plays = split_link[index].replace("\n",
                                                        "")  #\n isn't removed automatically, so I removed it manually

        else:  #Gives number of plays a value to avoid errors
            number_of_plays = None

        if number_of_plays is not None:  #Skips the process if number of plays doesn't exist
            while number_of_plays.startswith(" "):
                number_of_plays = number_of_plays.lstrip(" ")  #Removes spaces from the start

        plays_list.append(number_of_plays)

    entry_play_list = []

    for i in range(len(entry_list)):  #Creates a list alternating between artist/album names and their number of fails
        entry_play_list.append(entry_list[i])
        entry_play_list.append(plays_list[i])
    griddata = {}
    for i in range(0, len(entry_play_list), 2):
        griddata[entry_play_list[i]] = entry_play_list[i + 1]
        #Converts list to dictionary
    return griddata


#Process to get song data

song_tds = [td for td in
                      soup.find_all('td',
                                    class_="chartlist-name")]  #A list of all td elements with this class

initial_a_list = [td.find_all('a') for td in
                      song_tds]  #All links within the td elements
song_list = []

for a in initial_a_list:
    link = str(a)
    link = link.replace("<", ">")
    split_link = link.split(">")
    song_list.append(split_link[2])
    print(split_link[2])


artists = get_grid_data(get_config_data("number_of_artists"), 2)  #Index numbers acquired through trial and error

artist_list = []  #Used to clean up artist names from the output of the album dictionary
for key in artists.keys():
    artist_list.append(key)

albums = get_grid_data(int(get_config_data("number_of_artists") + get_config_data("number_of_albums")),
                       6)  #Index numbers acquired through trial and error
for key in artist_list:
    albums.pop(key)

with open('Last.fm.txt', 'w') as f:  #Writes data to txt file

    print(f"Last.fm profile data for user: {get_config_data("username")}: \n", file=f)
    print("Artist data:\n{", file=f)
    for key in artists:
        print(key, ' : ', artists[key], file=f)
    print("}\n", file=f)

    print("Album data:\n{", file=f)
    for key in albums:
        print(key, ' : ', albums[key], file=f)
    print("}\n", file=f)
