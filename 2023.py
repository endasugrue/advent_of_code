import requests
from util import setup_logging
import logging
from script_secrets import Secrets
import re
from collections import defaultdict
from pprint import pprint, pformat
from functools import reduce
import sys
import time
import numpy as np

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
                   logger.debug(f"{game_id}: new minimun for {colour}, as {int(amount)} > {min_cubes[colour]=}")
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
            logger.debug(f"{index=}, {value=}, {min_adj_index=}, {max_adj_index=}")
            # Scan row above
            if index != 0:
                row_above = input_as_list[index - 1]
                area_to_check_for_symbol_above = row_above[min_adj_index:max_adj_index]
                logger.debug(f"{area_to_check_for_symbol_above=}")
                for c in area_to_check_for_symbol_above:
                    if c in symbols_in_input_file:
                        logger.debug(f"Symbol {c} found in {area_to_check_for_symbol_above}")
                        numbers_to_be_added.append(value)

            # Current row
            area_to_check_for_symbol_current = row[min_adj_index:max_adj_index]
            logger.debug(f"{area_to_check_for_symbol_current}")
            for c in area_to_check_for_symbol_current:
                if c in symbols_in_input_file:
                    logger.debug(f"Symbol {c} found in {area_to_check_for_symbol_current}")
                    numbers_to_be_added.append(value)

            # Row below
            if index < len(input_as_list)-1:
                row_below = input_as_list[index + 1]
                area_to_check_for_symbol_below = row_below[min_adj_index:max_adj_index]
                logger.debug(f"{area_to_check_for_symbol_below=}")
                for c in area_to_check_for_symbol_below:
                    if c in symbols_in_input_file:
                        logger.debug(f"Symbol {c} found in {area_to_check_for_symbol_below}")
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
            logger.debug(f"{row[start_index:fin_index]}, {value}, {index}")
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
                logger.debug(f"Number found adjacent on line above {num}, {gear_index=}")
                numbers_to_be_multiplied.append(num.get("value"))
        
        for num in numbers_on_current_line:
            if (gear_index >= num.get("start_index")) and (gear_index <= num.get("fin_index")):
                logger.debug(f"Number found adjacent on current line {num}, {gear_index=}")
                numbers_to_be_multiplied.append(num.get("value"))

        for num in numbers_on_line_below:
            if (gear_index >= num.get("start_index")) and (gear_index <= num.get("fin_index")):
                logger.debug(f"Number found adjacent on line below {num}, {gear_index=}")
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
        logger.debug(f"{nums_i_have=}")
        logger.debug(f"{card=}, {card_value=}")
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
        logger.debug(f"{card_number=}, {data=}")
        for i in range(data.get("copies")):
            for m in range(1,data.get("number_of_matches")+1):
                # Do not attempt to have logging to stdout in this loop, it will crash your pc.
                cards_len_matches_copies[card_number + m]["copies"] += 1
    
    return sum([v.get("copies") for k,v in cards_len_matches_copies.items()])

def day_5_1(input:str) -> int:

    def calculate_for_individual_almananc(source_val, almananc):
        relevant_map = [m for m in almananc if m.get('source_start') <= source_val <= m.get('source_end')]
        if relevant_map == []:
            return source_val
        relevant_map = relevant_map[0]
        source_val_diff_from_start = source_val - relevant_map.get('source_start')
        corresponding_dest = relevant_map.get('dest_start') + source_val_diff_from_start
        return corresponding_dest
    
    def send_back_values_with_generator(seeds):
        for seed in seeds:
            time.sleep(0.01)
            soil = calculate_for_individual_almananc(seed,individual_almanacs['seed-to-soil'])
            fertilizer = calculate_for_individual_almananc(soil,individual_almanacs['soil-to-fertilizer'])
            water = calculate_for_individual_almananc(fertilizer,individual_almanacs['fertilizer-to-water'])
            light = calculate_for_individual_almananc(water,individual_almanacs['water-to-light'])
            temperature = calculate_for_individual_almananc(light,individual_almanacs['light-to-temperature'])
            humidity = calculate_for_individual_almananc(temperature,individual_almanacs['temperature-to-humidity'])
            location = calculate_for_individual_almananc(humidity,individual_almanacs['humidity-to-location'])

            yield {
                "seed":seed,
                "soil":soil,
                "fertilizer":fertilizer,
                "water":water,
                "light":light,
                "temperature":temperature,
                "humidity": humidity,
                "location": location
                }


    seeds = map(int,re.search(r"seeds: (.*?)\n\n", input).group(1).split(" "))
    individual_almanacs = {}
    maps = re.findall(r"(\w+-to-\w+) map", input)
    
    for m in maps:
        pattern = re.compile(fr"{m} map:\n(.*?)(?:\n\n|$)",re.DOTALL)
        string_values = re.search(pattern, input).group(1).split("\n")
        individual_almanacs[m] = []
        for s_val in string_values:
            dest_start,source_start,_range = map(int,s_val.split(" "))
            dest_end, source_end = (dest_start+_range -1, source_start+_range-1)
            individual_almanacs[m].append({
                "dest_start":dest_start,
                "dest_end":dest_end,
                "source_start":source_start,
                "source_end":source_end,
                "range":_range})
    
    combined_almanacs = [a for a in send_back_values_with_generator(seeds)]
        
    return min([a.get("location") for a in combined_almanacs])

def day_5_2(input:str) -> int:

    def get_seed_ranges_list(seeds):
        for i in range(0,len(seeds),2):
        
            yield range(seeds[i],seeds[i]+seeds[i+1])
    

    seeds = list(map(int,re.search(r"seeds: (.*?)\n\n", input).group(1).split(" ")))
    seed_ranges = [r for r in get_seed_ranges_list(seeds)]
    all_mins = []
    cmp_rgx_map_names = r"(\w+-to-\w+) map"
    
    for seed_range in seed_ranges[0:1]:
        logger.info(f"{seed_range=}")
        individual_almanacs = {}
        
        maps = re.findall(cmp_rgx_map_names, input)
        
        for m in maps:
            pattern = re.compile(fr"{m} map:\n(.*?)(?:\n\n|$)",re.DOTALL)
            string_values = re.search(pattern, input).group(1).split("\n")
            individual_almanacs[m] = []
            for s_val in string_values:
                dest_start,source_start,_range = map(int,s_val.split(" "))
                dest_end, source_end = (dest_start+_range -1, source_start+_range-1)
                individual_almanacs[m].append({
                    "dest_start":dest_start,
                    "dest_end":dest_end,
                    "source_start":source_start,
                    "source_end":source_end,
                    "range":_range})
        
        print(individual_almanacs['seed-to-soil'])
        break
        # lowest_in_ranges = min([a.get("dest_start") for a in individual_almanacs['humidity-to-location']])

    # return min(all_mins)
    ...

if __name__ == "__main__":
    
    mode = sys.argv[1]

    if mode not in ['manual', 'auto']:
        raise ValueError("Mode not supported")

    if mode == 'manual':
        ## Manually define the functions you want to call in here e.g.:
        logger = logging.getLogger('advent_of_code.manual')
        day_5_input = get_input_for_day(5)
        day_5_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
        
        # day_5_1_answer = day_5_1(day_5_input)
        # logger.info(f"{day_5_1_answer=}")

        day_5_2_answer = day_5_2(day_5_input)
        logger.info(f"{day_5_2_answer=}")
        print(f"{day_5_2_answer=}")
    elif mode == 'auto':
        for i in range(1,26):
            try:
                logger = logging.getLogger(f'advent_of_code.day_{i}')
                day_input = get_input_for_day(i)
                part_1_func_name = f"day_{i}_1"
                part_2_func_name = f"day_{i}_2"
                part_1_answer_name = f"day_{i}_1_answer"
                part_2_answer_name = f"day_{i}_2_answer"

                logger.info(f"{part_1_answer_name}={locals()[part_1_func_name](day_input)}")
                logger.info(f"{part_2_answer_name}={locals()[part_2_func_name](day_input)}")
            except Exception as e:
                logger.warning(f"We have not gottent this far yet, {e}")
                sys.exit(0)

