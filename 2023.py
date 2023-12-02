import requests
from util import setup_logging
import logging
from script_secrets import Secrets
import re
from collections import defaultdict

setup_logging('advent_of_code')
logger = logging.getLogger('advent_of_code')
secrets = Secrets()


def get_input_for_day(day:int) -> str:
    url = f"https://adventofcode.com/2023/day/{day}/input"
    cookies = {"session": secrets.aoc_session_token}
    req = requests.get(url, cookies=cookies)
    if req.status_code == 200:
        return req.text
    else:
        raise ValueError(f"Unable to get input for {day=}")

def day_1_1(input:str) -> int:
    input_as_list = input.strip().split("\n")
    input_digits_only = list(map(lambda x: re.sub(r"[^\d]",'',x),input_as_list))
    first_last = [f"{x[0]}{x[-1]}" for x in input_digits_only]
    total = sum(map(int, first_last))
    return total

def day_1_2(input:str) -> int:
    number_map = {"one":"on1e", "two":"tw2o", "three":"thre3e", "four":"fou4r", "five":"fiv5e", "six":"si6x", "seven":"seve7n", "eight":"eigh8t", "nine":"nin9e"}
    input_as_list = input.strip().split("\n")
    for k,v in number_map.items():
        input_as_list = list(map(lambda x: x.replace(k,v), input_as_list))
    input_digits_only = list(map(lambda x: re.sub(r"[^\d]",'',x),input_as_list))
    
    first_last = [f"{x[0]}{x[-1]}" for x in input_digits_only]
    logger.debug(first_last)
    total = sum(map(int, first_last))
    return total

def day_2_1(input:str) -> int:
    list_of_possible_games = []
    max_cubes = {"red":12,"green":13,"blue":14}
    input_as_list = input.strip().split("\n")
    for row in input_as_list:
        game_possible = True
        game_id, data = row.split(":")
        for set in data.split(";"):
            cubes = list(map(lambda x: x.strip(),set.split(",")))
            for cube in cubes:
                amount,colour = cube.split(' ')
                if int(amount) > max_cubes[colour]:
                    logger.debug(f"game not possible - {game_id}, too many {colour} cubes:{amount}")
                    game_possible = False
                    break

            if game_possible == False:
                break
        if game_possible:
            list_of_possible_games.append(game_id)
    return sum(map(lambda x: int(x.replace("Game ",'')),list_of_possible_games))

def day_2_2(input:str) -> int:
    min_cubes_powers = []
    
    input_as_list = input.strip().split("\n")
    for row in input_as_list:
        min_cubes = {"red":0,"green":0,"blue":0}
        game_id, data = row.split(":")
        for set in data.split(";"):
            cubes = list(map(lambda x: x.strip(),set.split(",")))
            for cube in cubes:
                amount,colour = cube.split(' ')
                if int(amount) > min_cubes[colour]:
                   logger.info(f"{game_id}: new minimun for {colour}, as {int(amount)} > {min_cubes[colour]=}")
                   min_cubes[colour] = int(amount)
        min_cubes_powers.append((min_cubes["red"]*min_cubes["blue"]*min_cubes["green"]))
    return sum(min_cubes_powers)




if __name__ == "__main__":
    
    # Day 1
    logger = logging.getLogger('advent_of_code.day_1')
    day_1_input = get_input_for_day(1)
    
    day_1_1_answer = day_1_1(day_1_input)
    logger.info(f"{day_1_1_answer=}")

    day_1_2_answer = day_1_2(day_1_input)
    logger.info(f"{day_1_2_answer=}")

    # Day 2
    logger = logging.getLogger('advent_of_code.day_2')
    day_2_input = get_input_for_day(2)

    day_2_2_answer = day_2_1(day_2_input)
    logger.info(f"{day_2_2_answer=}")

    day_2_2_answer = day_2_2(day_2_input)
    logger.info(f"{day_2_2_answer=}")