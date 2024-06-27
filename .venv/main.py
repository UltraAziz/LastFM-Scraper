import json
from bs4 import BeautifulSoup
import requests

counter = 0  #Self-explanatory, counts how many times a loop is executed


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


main_text_divs = [div for div in
                  soup.find_all('div', class_="grid-items-item-details")]  #A list of all div elements with this class
initial_a_list = [div.find_all('a', class_="link-block-target") for div in
                  main_text_divs]  #All links within the div elements
artist_list = []

for a in initial_a_list:
    link = str(a)  #Stores the a element as a string
    split_link = link.split('"')  #Splits links at every quotation mark
    artist_list.append(split_link[5])  #Adds the artist name to the artist list
    # (Artist name has the index [5] after splitting the links
    counter += 1
    if counter == int(get_config_data("number_of_artists")):
        break  #Stops the loop when it goes through all the artists

aux_test_p = [p for p in soup.find_all('p', class_="grid-items-item-aux-text")]  #List of p elements with that class
a_list = [p.find_all('a') for p in aux_test_p]  #Links within those p elements

plays_list = []

for a in a_list:
    link = str(a)
    link = link.replace('<', '>')  #For easier splitting
    split_link = link.split('>')
    number_of_plays = split_link[2].replace("\n", "")  #\n isn't removed automatically, so I removed it manually
    while number_of_plays.startswith(" "):
        number_of_plays = number_of_plays.lstrip(" ")  #Removes spaces from the start

    plays_list.append(number_of_plays)

artist_play_list = []

for i in range(len(artist_list)):
    artist_play_list.append(artist_list[i])
    artist_play_list.append(plays_list[i])
    #Creates a list alternating between artist names and their number of fails

artists = {}
for i in range(0, len(artist_play_list), 2):
    artists[artist_play_list[i]] = artist_play_list[i + 1]
    #Converts list to dictionary

with open('Last.fm.txt', 'w') as f:  #Writes data to txt file
    print(f"Last.fm profile data for user: {get_config_data("username")}: \n", file=f)
    print("Artist data:\n{", file=f)
    for key in artists:
        print(key, ' : ', artists[key], file=f)
    print("}\n", file=f)
