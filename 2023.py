import requests
from util import setup_logging
import logging
from script_secrets import Secrets
import re
from collections import defaultdict
from pprint import pprint, pformat
from functools import reduce

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
        logger.error(req.text)
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

def day_3_1(input:str) -> int:
    input_as_list = input.strip().split("\n")
    symbols_in_input_file = "*#-+@%&=$/"
    line_symbols_data = {}
    line_number_data = {}
    numbers_to_be_added = []
    for index,row in enumerate(input_as_list):
        line_symbols_data[index] = []
        line_number_data[index] = []
        numbers = re.finditer(r"\d+", row)
        for num in numbers:
            value = num.group(0)
            min_adj_index = num.start(0) - 1 if (num.start(0) - 1) > 0 else 0
            max_adj_index = num.end(0) + 1
            logger.info(f"{index=}, {value=}, {min_adj_index=}, {max_adj_index=}")
            # Scan row above
            if index != 0:
                row_above = input_as_list[index - 1]
                area_to_check_for_symbol_above = row_above[min_adj_index:max_adj_index]
                logger.info(f"{area_to_check_for_symbol_above=}")
                for c in area_to_check_for_symbol_above:
                    if c in symbols_in_input_file:
                        logger.info(f"Symbol {c} found in {area_to_check_for_symbol_above}")
                        numbers_to_be_added.append(value)

            # Current row
            area_to_check_for_symbol_current = row[min_adj_index:max_adj_index]
            logger.info(f"{area_to_check_for_symbol_current}")
            for c in area_to_check_for_symbol_current:
                if c in symbols_in_input_file:
                    logger.info(f"Symbol {c} found in {area_to_check_for_symbol_current}")
                    numbers_to_be_added.append(value)

            # Row below
            if index < len(input_as_list)-1:
                row_below = input_as_list[index + 1]
                area_to_check_for_symbol_below = row_below[min_adj_index:max_adj_index]
                logger.info(f"{area_to_check_for_symbol_below=}")
                for c in area_to_check_for_symbol_below:
                    if c in symbols_in_input_file:
                        logger.info(f"Symbol {c} found in {area_to_check_for_symbol_below}")
                        numbers_to_be_added.append(value)
            
    return sum(map(int,numbers_to_be_added))

def day_3_2(input:str) -> int:
    
    input_as_list = input.strip().split("\n")
    gear_data = []
    number_data = []
    numbers_to_be_added = []
    for index,row in enumerate(input_as_list):
        numbers = re.finditer(r"\d+", row)
        for num in numbers:
            value = num.group(0)
            start_index = num.start(0)-1 if num.start(0) -1 > 0 else 0
            fin_index = num.end(0)
            number_data.append({"index": index, "value":value, "start_index": start_index, "fin_index": fin_index})
            print(row[start_index:fin_index], value, index)
        gears = re.finditer(r"\*", row)
        for gear in gears:
            gear_data.append({"line_index": index, "gear_index": gear.start(0)})
    
    for g in gear_data:
        numbers_to_be_multiplied = []
        line_index = g.get("line_index")
        gear_index = g.get("gear_index")
        
        #Line above
        numbers_on_line_above = [n for n in number_data if n.get("index") == line_index -1]
        numbers_on_current_line = [n for n in number_data if n.get("index") == line_index]
        numbers_on_line_below = [n for n in number_data if n.get("index") == line_index+1]

        for num in numbers_on_line_above:
            if (gear_index >= num.get("start_index")) and (gear_index <= num.get("fin_index")):
                logger.info(f"Number found adjacent on line above {num}, {gear_index=}")
                numbers_to_be_multiplied.append(num.get("value"))
        
        for num in numbers_on_current_line:
            if (gear_index >= num.get("start_index")) and (gear_index <= num.get("fin_index")):
                logger.info(f"Number found adjacent on current line {num}, {gear_index=}")
                numbers_to_be_multiplied.append(num.get("value"))

        for num in numbers_on_line_below:
            if (gear_index >= num.get("start_index")) and (gear_index <= num.get("fin_index")):
                logger.info(f"Number found adjacent on line below {num}, {gear_index=}")
                numbers_to_be_multiplied.append(num.get("value"))
        
        if len(numbers_to_be_multiplied) == 2:
            numbers_to_be_added.append(int(numbers_to_be_multiplied[0])*int(numbers_to_be_multiplied[1]))

    
    return sum(numbers_to_be_added)


def day_4_1(input:str) -> int:
    input_as_list = input.strip().split("\n")
    card_values = []
    for row in input_as_list:
        card_value = 0
        card, data = row.split(":")
        str_win, str_my_nums = data.split("|")
        set_winning= set([n.group(0) for n in re.finditer(r"\d+", str_win)])
        set_my_nums = set([n.group(0) for n in re.finditer(r"\d+", str_my_nums)])
        nums_i_have = set_winning.intersection(set_my_nums)
        for i in range(len(nums_i_have)):
            if i == 0:
                card_value = 1
            else:
                card_value *= 2
        logger.info(f"{nums_i_have=}")
        logger.info(f"{card=}, {card_value=}")
        card_values.append(card_value)

    return sum(card_values)

def day_4_2(input:str) -> int:
    input_as_list = input.strip().split("\n")
    cards_len_matches_copies = {}
    for row in input_as_list:
        card, data = row.split(":")
        card = int(re.search(r"\d+",card).group(0))
        str_win, str_my_nums = data.split("|")
        set_winning= set([n.group(0) for n in re.finditer(r"\d+", str_win)])
        set_my_nums = set([n.group(0) for n in re.finditer(r"\d+", str_my_nums)])
        nums_i_have = set_winning.intersection(set_my_nums)
        cards_len_matches_copies[card] = {"number_of_matches": len(nums_i_have),"copies": 1}

    for card_number, data in cards_len_matches_copies.items():
        logger.info(f"{card_number=}, {data=}")
        for i in range(data.get("copies")):
            for m in range(1,data.get("number_of_matches")+1):
                # Do not attempt to have logging to stdout in this loop, it will crash your pc.
                cards_len_matches_copies[card_number + m]["copies"] += 1
    
    return sum([v.get("copies") for k,v in cards_len_matches_copies.items()])




if __name__ == "__main__":
    
    # # Day 1
    # logger = logging.getLogger('advent_of_code.day_1')
    # day_1_input = get_input_for_day(1)
    
    # day_1_1_answer = day_1_1(day_1_input)
    # logger.info(f"{day_1_1_answer=}")

    # day_1_2_answer = day_1_2(day_1_input)
    # logger.info(f"{day_1_2_answer=}")

    # # Day 2
    # logger = logging.getLogger('advent_of_code.day_2')
    # day_2_input = get_input_for_day(2)

    # day_2_1_answer = day_2_1(day_2_input)
    # logger.info(f"{day_2_1_answer=}")

    # day_2_2_answer = day_2_2(day_2_input)
    # logger.info(f"{day_2_2_answer=}")

    # # Day 3
    # logger = logging.getLogger('advent_of_code.day_3')
    # day_3_input = get_input_for_day(3)


    # day_3_1_answer = day_3_1(day_3_input)
    # logger.info(f"{day_3_1_answer=}")

    # day_3_2_answer = day_3_2(day_3_input)
    # logger.info(f"{day_3_2_answer=}")

    # Day 4
    logger = logging.getLogger('advent_of_code.day_4')
    day_4_input = get_input_for_day(4)

#     day_4_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


    # day_4_1_answer = day_4_1(day_4_input)
    # logger.info(f"{day_4_1_answer=}")

    day_4_2_answer = day_4_2(day_4_input)
    logger.info(f"{day_4_2_answer=}")