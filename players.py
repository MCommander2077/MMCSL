import requests
import json


def get_players_from_data(data):
    data = data.split(':')
    data = data[1][1:]
    data = data.split(', ')
    return data


def get_player_info(player):
    json_uuid = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{player}').text
    uuid = json.loads(json_uuid)['id']
    # https://starlightskins.lunareclipse.studio/skin-render/relaxing/{player}/full
    skin_file = requests.get(f'https://starlightskins.lunareclipse.studio/skin-render/relaxing/{player}/full').text
    data = {
        'name': player,
        'uuid': uuid,
        'skin': skin_file,
    }
    return data


def player_operate(player, operate):
    if operate == 'b':
        return f'ban {player}'
    elif operate == 'k':
        return f'kick {player}'
    elif operate == 'i':
        return get_player_info(player)


if __name__ == '__main__':
    print(get_players_from_data('[info]There are 2 of a max of 20 players online: abdeffff, MCommander2077'))
    print(get_player_info('MCommander2077')['name'], get_player_info('MCommander2077')['uuid'])
