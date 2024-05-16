import requests
from bs4 import BeautifulSoup
import csv

# Global variables for urls to grab files from
MOVES_URL = 'https://bulbapedia.bulbagarden.net/wiki/List_of_moves'
POKEMON_URL = 'https://pokemon.fandom.com/wiki/Category:Generation_I_Pok%C3%A9mon'
NUM_MOVES = 165

def read_moves(url, num_moves = 165):
    """
    Reads in move data from master url

    :param url (str): link to bulbapedia list of moves
    :return: None
    """
    print('Initializing!')

    # Initializes lists to hold data
    links = []
    names = []
    types = []
    categories = []
    pp = []
    power = []
    accuracy = []
    desc = []

    # Scrapes master link for sublinks to individual moves
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    moves = soup.find_all('a', {'title': lambda L: L and L.endswith('(move)')})
    for move in moves:
        links.append('https://bulbapedia.bulbagarden.net/wiki/' + move['href'][6:])
        names.append(move['title'][:-7].replace(" ", "").replace('-', ''))

    for i in range(num_moves + 1):
        # Scrapes sublink for info on a single move
        print(f'Move {i+1} read!')
        html = requests.get(links[i]).text
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table', {'style': lambda L: L and L.startswith('float:right;')})
        table = table.find('table')

        # Gets simple stats from right hand table
        stats = table.find_all('td')
        types.append(stats[0].text.strip())
        categories.append(stats[1].text.strip())
        move_pp = stats[2].text.strip()
        move_pp = int(move_pp[:move_pp.index(' ')])
        pp.append(move_pp)

        # Gets move power from table
        move_power = stats[3].text.strip()
        if move_power == '—' or move_power == 'Varies':
            move_power = 0
        else:
            move_power = int(move_power)
        power.append(move_power)

        # Gets move accuracy from table
        move_accuracy = stats[4].text.strip()
        move_accuracy = move_accuracy[:move_accuracy.index('%')]
        if move_accuracy == '—':
            move_accuracy = 0
        else:
            move_accuracy = float(move_accuracy) / 100
        accuracy.append(move_accuracy)

        # Gets rudimentary description for Gen 1 information
        p = soup.find('p').text.strip() + ' ' + soup.find('h2').find_next('h2').find_next('p').text.strip()
        p = p.replace('\n', '')
        p = p.replace(',', ';')
        desc.append(p)

    # Rearranges data in csv-friendly format
    print('Sorting!')
    data = []
    for i in range(num_moves):
        data.append([i, names[i], types[i], categories[i], pp[i], power[i],
                     accuracy[i], desc[i], links[i], names[i].lower()])

    # Creates csv housing data for easy object creation
    print('Writing csv!')
    header = ['Index', 'Name', 'Type', 'Category', 'PP', 'Power', 'Accuracy', 'Desc', 'Link']
    with open('data/moves.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    print('Done!')

def read_pokemon(url):
    """
    Webscrapes pokemon data

    :param url:
    :return:
    """
    print('Intializing!')

    # Initializes lists to hold data
    names = []
    health = []
    attack = []
    defense = []
    spatt = []
    spdef = []
    speed = []
    movesets = []
    types = []
    images = []

    html = requests.get('https://www.pokencyclopedia.info/en/index.php?id=sprites/gen5/ani_black-white').text
    soup = BeautifulSoup(html, 'lxml')
    test = soup.find_all('table', {'class': 'spr'})
    for t in test:
        m = t.find('img')
        images.append('https://www.pokencyclopedia.info' + m['src'][2:])

    # Scrapes master link to get all pokemon names
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    test = soup.find_all('div', {'class': 'lightbox-caption'})
    for t in test:
        names.append(t.find('a')['title'])

    # Scrapes secondary link to get info on each individual pokemon
    for pokemon in names:
        print(f'Pokemon {names.index(pokemon) + 1} read!')
        html = requests.get(f'https://pokemon.fandom.com/wiki/{pokemon}#Generation_I').text
        soup = BeautifulSoup(html, 'lxml')

        # Gets basic stats
        table = soup.find('table', {'class': 'roundy'})
        stats = table.find_all('b')
        print(stats.text)
        health.append(int(stats[2].text))
        attack.append(int(stats[4].text))
        defense.append(int(stats[6].text))
        # spatt.append(int(stats[8].text))
        # spdef.append(int(stats[10].text))
        speed.append(int(stats[12].text))

        # Gets pokemon types
        pokemon_types = []
        sidebar = soup.find('aside')
        sidebar = sidebar.find('div', {'data-source': 'type'})
        sidebar = sidebar.find('div', {'class': lambda L: L and L.startswith('pi-data-value')})
        sidebar = sidebar.find_all('a')
        for s in sidebar:
            pokemon_types.append(s['title'][:-5])
        pokemon_types = ';'.join(pokemon_types)
        types.append(pokemon_types)


        # Gets moves that pokemon can use (through learning / HM / TM)
        name = pokemon.replace("'", "").replace('.', '').replace(' ', '-').replace('♀', '-f').replace('♂', '-m')
        moveset = []
        html = requests.get(f'https://pokemondb.net/pokedex/{name.lower()}/moves/1').text
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.find_all('tbody')
        tables = tables[:min(4, len(tables))]
        for table in tables:
            moves = table.find_all('td', {'class': 'cell-name'})
            for move in moves:
                if move.text not in moveset:
                    moveset.append(move.text.replace(" ", '').replace('-', ''))
        moveset = list(set(moveset))
        moveset = ';'.join(moveset)
        movesets.append(moveset)

    html = requests.get('https://pokemondb.net/pokedex/stats/gen1').text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('tbody').find_all('tr')
    for tr in table:
        cells = tr.find_all('td')
        spatt.append(int(cells[7].text))
        spdef.append(int(cells[8].text))

    # Rearranges data in csv-friendly format
    print('Sorting!')
    data = []
    for i in range(len(names)):
        data.append([i + 1, names[i], types[i], health[i], attack[i], defense[i],
                     spatt[i], spdef[i], speed[i], movesets[i], images[i], names[i].lower()])

    # Creates csv housing data for easy object creation
    print('Writing csv!')
    header = ['Pokedex', 'Name', 'Types', 'Health', 'Attack', 'Defense',
              'Special Attack', 'Special Defense', 'Speed', 'Movesets', 'Image']
    with open('data/pokemon.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    print('Done!')

# Functions to call if we need to recreate files
# read_moves(MOVES_URL)
# read_pokemon(POKEMON_URL)
