#!/usr/bin/python3

import ast
import requests
import json
from numpy import dot
from numpy.linalg import norm

string1 = input("Enter the first string: ")
string2 = input("Enter the second string: ")
string3 = input("Enter the third string: ")

print("You entered: ")
print(string1)
print(string2)
print(string3)


board_1_id = "vlmalealgte"
board_2_id = "yitmmvkesme"
first_baselines = [0.07814215,  0.01657072,  0.9529908, 0.07943136, -0.96086917, -0.05101767,
                   -0.00669531,  0.88141954, -0.01597478,  0.09528435,  0.04982841, -0.04149313,
                   0.02369967, -0.01994463,  0.08883739]
second_baselines = [-9.47114780e-01, -3.52115273e-02, -9.70982683e-01,  9.92304548e-02,
                    5.59859687e-02,  6.41062358e-02,  6.61199914e-02,  2.66244628e-02,
                    1.94398568e-02,  7.92623274e-02, -7.23194838e-05, -9.70542452e-01,
                    -2.41675214e-02, -7.36960329e-02, -4.03905303e-03]


def str_list_to_float_list(string_list):
    try:
        int_list = [float(num) for num in string_list]
        return int_list
    except ValueError:
        raise ValueError(
            "One or more elements of the list are not valid integers.")


def string_list_str_to_float_list(string_list_str):
    try:
        string_list = ast.literal_eval(string_list_str)
        int_list = str_list_to_float_list(string_list)
        return int_list
    except (SyntaxError, ValueError) as e:
        print(f"Error: {e}")


def create_user(user_name, endpoint):
    create_user_api_endpoint = 'https://keepthescore.co/api/{id}/player/'
    create_user_api_endpoint = create_user_api_endpoint.format(id=endpoint)
    data = {"name": user_name}
    response = requests.post(create_user_api_endpoint, json=data)
    return find_player_id(response.text, user_name)


def find_player_id(json_string, player_name):
    try:
        # Parse the JSON string into a Python object
        data = json.loads(json_string)

        # Loop through the players and find the player with the specified name
        for player in data['players']:
            if player['name'] == player_name:
                return player['id']
        else:
            return None

    except (json.JSONDecodeError, KeyError) as e:
        print('Error:', e)
        return None


def calculate_score(board_id, user_id, base_line, result):
    sim = dot(base_line, result)/(norm(base_line)*norm(result))
    print(base_line)
    print(result)
    print(sim)
    update_score_api_endpoint = 'https://keepthescore.co/api/{id}/score/'
    update_score_api_endpoint = update_score_api_endpoint.format(id=board_id)
    data = {"player_id": user_id, "score": sim*100}

    response = requests.post(update_score_api_endpoint, json=data)


team_name = string1
first_set = string2
second_set = string3
first = string_list_str_to_float_list(first_set)
second = string_list_str_to_float_list(second_set)

if len(first) == 15:
    id1 = create_user(team_name, board_1_id)
    calculate_score(board_1_id, id1, first_baselines, first)

if len(second) == 15:
    id2 = create_user(team_name, board_2_id)
    calculate_score(board_2_id, id2, second_baselines, second)
