import os
from enum import Enum
import json
import random


class EncounterChoice:
    def __init__(self):
        self.option_text = ""
        self.good_outcome_text = ""
        self.bad_outcome_text = ""
        self.good_outcome = {"food": 0, "water": 0, "happiness": 0, "economy": 0}
        self.bad_outcome = {"food": 0, "water": 0, "happiness": 0, "economy": 0}
        self.good_chance = 0  # chance for good outcome out of 100

    def __init__(self, p_o_text, gd_text, bd_text, gd_out, bd_out, gd_chance):
        self.option_text = p_o_text
        self.good_outcome_text = gd_text
        self.bad_outcome_text = bd_text
        self.good_outcome = gd_out
        self.bad_outcome = bd_out
        self.good_chance = gd_chance


class Encounter:
    def __init__(self):
        self.encounter_name = ""
        self.encounter_memo = ""
        self.choices = []

    def roll_encounter(self, p_choice_num):
        x = random.randint(1, 100)
        if x < self.choices[p_choice_num].good_chance:
            # good outcome
            return self.choices[p_choice_num].good_outcome_text, self.choices[p_choice_num].good_outcome
        else:
            # bad outcome
            return self.choices[p_choice_num].bad_outcome_text, self.choices[p_choice_num].bad_outcome

    def add_choice(self, p_o_text, gd_text, bd_text, gd_out, bd_out, gd_chance):
        temp_choice = EncounterChoice(p_o_text, gd_text, bd_text, gd_out, bd_out, gd_chance)
        self.choices.append(temp_choice)

    def append_choice_object(self, p_object):
        self.choices.append(p_object)


class BuildingTypeId(Enum):
    FARM = 1
    MOSQUE = 2
    WELL = 3
    MARKET = 4


class Building:
    def __init__(self, p_building_type):
        if p_building_type == BuildingTypeId.FARM:
            self.building_name = "Farm"
            self.food_mod = 25
            self.water_mod = -10
            self.population_growth_percent_mod = 1
            self.happiness_mod = 0
            self.economy_mod = 1
            self.building_price = 10
        if p_building_type == BuildingTypeId.MOSQUE:
            self.building_name = "Mosque"
            self.food_mod = 0
            self.water_mod = 0
            self.population_growth_percent_mod = 0
            self.happiness_mod = 2
            self.economy_mod = -1
            self.building_price = 20
        if p_building_type == BuildingTypeId.WELL:
            self.building_name = "Well"
            self.food_mod = 0
            self.water_mod = 15
            self.population_growth_percent_mod = 1
            self.happiness_mod = 0
            self.economy_mod = 0
            self.building_price = 10
        if p_building_type == BuildingTypeId.MARKET:
            self.building_name = "Market"
            self.food_mod = -10
            self.water_mod = -10
            self.population_growth_percent_mod = 1
            self.happiness_mod = 1
            self.economy_mod = 2
            self.building_price = 15

class City:
    def __init__(self, p_name):
        self.name = p_name
        self.population = 100
        self.population_growth_percent_base = 5
        self.food = 300
        self.water = 300
        self.happiness = 70
        self.troops = 0  # maybe
        self.economy = 5
        self.spending_food = 0
        self.spending_water = 0
        self.buildings = list()
        self.spending_troops = 0  # maybe
        self.trades = list()    # maybe

    def build_building(self, p_building_type_id):
        self.buildings.append(Building(p_building_type_id))

    def show_status(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Name: " + self.name + " | Pop: " + str(self.population) + "\nFood: " + str(self.food) + " | Water: "
               + str(self.water) + "\nHappiness: " + str(self.happiness) + " | Economy Size: " + str(self.economy))
        print("----------------------------------------------------")
        print("Buildings:")
        for bldg in self.buildings:
            print(bldg.building_name)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


class Player:
    def __init__(self):
        self.name = ""
        self.wealth = 0
        self.cities = list()

    def create_city(self, p_name):
        temp_city = City(p_name)
        temp_city.name = p_name
        self.cities.append(temp_city)

    def show_status(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Name: " + self.name + " | Wealth: " + str(self.wealth))
        print("----------------------------------------------------")
        print("Cities:")
        for city in self.cities:
            print(city.name + " | P:" + str(city.population) + " | F:" + str(city.food) + " | W:"
                  + str(city.water) + " | H: " + str(city.happiness) + " | E: " + str(city.economy))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


class GameEngine:
    def __init__(self):
        self.engine_running = False
        self.turn = 1
        self.max_turns = 20
        self.months_per_turn = 6
        self.end_year = 1120
        self.end_month = 12
        self.year = 1100
        self.month = 1
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                       "October", "November", "December"]
        self.local_player = Player()
        self.local_player_cities = ""
        self.multiplayer_cities = list()  # maybe just maybe
        self.message_buffer = []
        self.high_score = []
        self.game_over_flag = False
        self.encounters_deck = []
        self.random_encounter_flag = False

    def show_game_status(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Month: " + self.months[self.month - 1] + " | Year: " + str(self.year))
        print("Turn " + str(self.turn) + " of " + str(self.max_turns))
        print("----------------------------------------------------")
        print("Letters From Around Your Empire:")
        if len(self.message_buffer) == 0:
            print("Nothing to report...")
        else:
            for msg in self.message_buffer:
                print(msg)

    def game_start(self):
        self.LoadHighScore()
        self.engine_running = True
        self.local_player.name = "Sultan"
        self.local_player.wealth = 100
        self.local_player.create_city("Sultania")
        self.generate_encounters()
        self.game_loop()

    def LoadHighScore(self):
        try:
            with open("highscore.json", "r") as read_file:
                data = json.load(read_file)
            self.high_score = data["highscore"]
        except FileNotFoundError:
            self.high_score = 0

    def GetInput(self):
        input_valid = True
        while input_valid:
            self.show_game_status()
            self.local_player.show_status()

            # catch and handle the game over flag for forcing a break return after showing statuses.
            if self.game_over_flag:
                print("I am sorry, Sultan, but your time has ended...")
                self.engine_running = False
                return

            print("My Sultan, how may we serve you?")
            print("1) Cities\n2) Standings\n3) Let Time Pass\n4) Surrender To the Annals of Time")
            choice = input("Your bidding:")
            choice = int(choice)

            # Chose to view Cities
            if choice == 1:
                clear()
                print("Yes, my Sultan, you wish to see your loyal cities.")
                print("Which would you like to give orders to:")
                # List out the cities
                for num, city in enumerate(self.local_player.cities):
                    print(str(num + 1) + ") " + city.name + " | " + str(city.population))
                print(str(len(self.local_player.cities) + 1) + ") " + "Cancel")

                choice = input("Your Selection: ")
                choice = int(choice)
                if choice not in range(0, len(self.local_player.cities)+1):
                    print("What is it you need, Sultan")
                    continue

                # Take the selected city and run it.
                # first print out city info in depth
                selected_city_number = choice - 1
                self.local_player.cities[selected_city_number].show_status()
                # now show possible actions
                print("What action would you like to take, My Sultan?")
                print("1) Build a Building")
                # print("2) Destroy a Building")
                print("2) Seek an Encounter")
                # print("3) Buy This City Resources")
                # print("4) Sell Some of This City's Resources")
                # print("5) Raze This City to the Ground")
                print("6) Exit")
                choice = input("Your Bidding, Sultan: ")
                choice = int(choice)

                if choice == 1:
                    print("Build A Building:")
                    print("Your Available Wealth: " + str(self.local_player.wealth))
                    print("Buildings Available:")
                    print("1) Farm   | Price: " + str(Building(BuildingTypeId.FARM).building_price))
                    print("2) Mosque | Price: " + str(Building(BuildingTypeId.MOSQUE).building_price))
                    print("3) Well   | Price: " + str(Building(BuildingTypeId.WELL).building_price))
                    print("4) Market | Price: " + str(Building(BuildingTypeId.MARKET).building_price))
                    print("5) Exit")
                    choice = input("Your Bidding, Sultan: ")
                    choice = int(choice)
                    print("CHOICE: " + str(choice))
                    bldg_type = ""
                    if choice == 1:
                        bldg_type = BuildingTypeId.FARM
                    if choice == 2:
                        bldg_type = BuildingTypeId.MOSQUE
                    if choice == 3:
                        bldg_type = BuildingTypeId.WELL
                    if choice == 4:
                        bldg_type = BuildingTypeId.MARKET
                    if choice not in range(1, 5):
                        print("ELSE FIRED")
                        continue

                    # process build
                    if self.local_player.wealth < Building(bldg_type).building_price:
                        print("Alas, my Sultan, our coffers are to shallow...")
                        continue
                    print("HAD ENOUGH MONEY")
                    print("We shall build the " + Building(bldg_type).building_name + " immediately!")
                    self.local_player.wealth -= Building(bldg_type).building_price
                    self.local_player.cities[selected_city_number].build_building(bldg_type)
                    continue

                # if choice == 2:
                #    print("Destroy A Building:")
                if choice == 2:
                    print("Seek an Encounter:")
                    if self.random_encounter_flag:
                        print("I am sorry Sultan, no more encounters to find.")
                        continue
                    else:
                        roll = random.randint(0, len(self.encounters_deck) - 1)
                        selected_encounter = self.encounters_deck[roll]
                        print(":::ENCOUNTER:::")
                        print(selected_encounter.encounter_name)
                        print(selected_encounter.encounter_memo)
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print("CHOICES:")
                        print("--------")
                        for x, choice in enumerate(selected_encounter.choices):
                            print(str(x + 1) + ") " + choice.option_text)
                        while True:
                            choice = input("Please Choose:")
                            choice = int(choice) - 1
                            if choice in range(0, len(selected_encounter.choices)):
                                outcome = selected_encounter.roll_encounter(choice)
                                clear()
                                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                print(":::OUTCOME:::")
                                print(outcome[0])
                                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                self.local_player.cities[selected_city_number].food += outcome[1]["food"]
                                self.local_player.cities[selected_city_number].water += outcome[1]["water"]
                                self.local_player.cities[selected_city_number].happiness += outcome[1]["happiness"]
                                self.local_player.cities[selected_city_number].economy += outcome[1]["economy"]
                                self.random_encounter_flag = True
                                break
                        continue

                # if choice == 4:
                #    print("Buy Resources:")
                # if choice == 5:
                #     print("Sell Resources:")
                # if choice == 6:
                #    print("Raze The City:")
                if choice == 6:
                    print("As you wish, Sultan")
                    continue
                else:
                    print("I do not understand, Sultan")
                    continue

            if choice == 2:
                for player in self.standings:
                    print(player.name, player.score)
                continue

            if choice == 3:
                print("6 months pass....")
                # handle a turn
                return


            if choice == 4:
                print("Sultan, are you passing away from us?")
                choice = input("1) YES 2) NO")
                choice = int(choice)
                if choice == 1:
                    self.engine_running = False
                    input_valid = False
                else:
                    print("Whew, that was a close one Sultan...")
                    continue

    def calculate_score(self):
        score = 0
        score += self.turn * 100
        for city in self.local_player.cities:
            score += city.population * 1
            score += city.food
            score += city.water
            score += city.happiness
        return score

    def generate_encounters(self):
        print("")
        self.create_and_push_encounter("Bandits!",
                                       "Bandits are roving through your city,\nthe people cry out for your help!",
                                       [EncounterChoice("Send The Troops", "Army Stops Bandits", "Army Stops Bandits, but does damage",
                                                        {"food": 0, "water": 0, "happiness": 5, "economy": 0},
                                                        {"food": -5, "water": -5, "happiness": -5, "economy": -1},
                                                        80),
                                        EncounterChoice("Do Nothing", "Civilians Fend Them Off",
                                                        "City Ravaged",
                                                        {"food": 0, "water": 0, "happiness": -5, "economy": 0},
                                                        {"food": -10, "water": -10, "happiness": -10, "economy": -1},
                                                        5),
                                        ])

        self.create_and_push_encounter("Gold Rush!",
                                       "Some of your citizens have found gold in the hills, Sultan.\nWhat should we do?",
                                       [EncounterChoice("This Gold is the Sultan's!", "Economy is boosted!",
                                                        "The People Riot, destroying crops!",
                                                        {"food": 0, "water": 0, "happiness": -10, "economy": 5},
                                                        {"food": -25, "water": 0, "happiness": -15, "economy": 0},
                                                        50),
                                        EncounterChoice("Good For Them!", "Economy Booms!",
                                                        "Crime Sprees Break out over flood of money",
                                                        {"food": 0, "water": 0, "happiness": 10, "economy": 3},
                                                        {"food": -20, "water": -20, "happiness": -10, "economy": -1},
                                                        90),
                                        ])

        self.create_and_push_encounter("Rats in the Granary!",
                                       "Rats are in the grain bins, Sultan!\nWhat should we do?",
                                       [EncounterChoice("Burn the grain bins that are affected", "Grain Bins Burned",
                                                        "Fire Spreads, burning businesses!",
                                                        {"food": -10, "water": 0, "happiness": 0, "economy": 0},
                                                        {"food": -10, "water": 0, "happiness": -10, "economy": -1},
                                                        50),
                                        EncounterChoice("Rats go good with Oatmeal!", "RatMeal Catches on!",
                                                        "Well at least the rats are full...",
                                                        {"food": 10, "water": 0, "happiness": 3, "economy": 1},
                                                        {"food": -30, "water": 0, "happiness": -10, "economy": 0},
                                                        5),
                                        ])

        self.create_and_push_encounter("An Evil Uncle Returns!",
                                       "Sultan! Your Evil Uncle Francis has returned!\nHe is demanding the Sultanship.\nWhat should we do?",
                                       [EncounterChoice("I feel a flogging is in order, assert my dominance!", "Uncle Dissuaded",
                                                        "Citizen's view actions as unjust!",
                                                        {"food": 0, "water": 0, "happiness": 0, "economy": 0},
                                                        {"food": 0, "water": 0, "happiness": -5, "economy": 0},
                                                        50),
                                        EncounterChoice("Execute Him!", "Uncle's Head Rolls!",
                                                        "Uncle's Head Rolls, Citizen's view action as dishonorable",
                                                        {"food": 0, "water": 0, "happiness": 0, "economy": 0},
                                                        {"food": 0, "water": 0, "happiness": -10, "economy": 0},
                                                        30),
                                        EncounterChoice("Show him mercy, he is family after all!", "Uncle forms profitable turban business!",
                                                        "Uncle spreads lies and sows discontent",
                                                        {"food": 0, "water": 0, "happiness": 3, "economy": 1},
                                                        {"food": 0, "water": 0, "happiness": -15, "economy": 0},
                                                        30)
                                        ])

        self.create_and_push_encounter("We Found a forgotten crypt!",
                                       "We have stumbled on an ancient crypt!\nWhat should we do?",
                                       [EncounterChoice("Nope, I know how this ends, destroy the entrance", "Entrance Destroyed",
                                                        "Entrance collapses, sealing in unknown secrets",
                                                        {"food": 0, "water": 0, "happiness": 0, "economy": 0},
                                                        {"food": 0, "water": 0, "happiness": 0, "economy": 0},
                                                        50),
                                        EncounterChoice("Go in yourself", "You find treasures!",
                                                        "You fall in a pit and must be rescued, what a laugh...loss of respect though.",
                                                        {"food": 0, "water": 0, "happiness": 5, "economy": 3},
                                                        {"food": 0, "water": 0, "happiness": -5, "economy": 0},
                                                        40),
                                        EncounterChoice("Send In A Guard", "Guard finds treasures!",
                                                        "Guard finds treasures, then absconds through a secret pass with the loot...embarassing",
                                                        {"food": 0, "water": 0, "happiness": 3, "economy": 2},
                                                        {"food": 0, "water": 0, "happiness": -10, "economy": 0},
                                                        40)
                                        ])

    def create_and_push_encounter(self, p_name, p_memo, p_choices: list()):
        temp_encounter = Encounter()
        temp_encounter.encounter_name = p_name
        temp_encounter.encounter_memo = p_memo
        for choice in p_choices:
            temp_encounter.append_choice_object(choice)
        self.encounters_deck.append(temp_encounter)

    def end_game_process(self):
        clear()
        score = self.calculate_score()
        print ("The End has come, my Sultan...")
        print("You scored " + str(score))
        if score > self.high_score:
            print("This is the highest score, yet!")
            data = {"highscore": score}
            with open("highscore.json", "w") as write_file:
                json.dump(data, write_file)
        print("END OF GAME")

    def process_players(self):
        # calc earnings
        earnings = 0
        for city in self.local_player.cities:
            earnings += int(city.economy * (city.happiness/100))
        self.local_player.wealth += earnings
        self.message_buffer.append(str(earnings) + " gold has been added to the coffers, Sultan.")

        # calc food and water consumption and happiness changes
        for city in self.local_player.cities:
            happiness_change = 0
            population_mod = 0
            city.food -= city.population
            city.water -= city.population
            if city.food < 0:
                population_mod += city.food
                city.food = 0
                city.happiness -= 15
                self.message_buffer.append("Your people starve!")
            else:
                happiness_change += 1
            if city.water < 0:
                population_mod += city.water
                city.water = 0
                city.happiness -= 15
                self.message_buffer.append("Your people thirst!")
            else:
                happiness_change += 1
            if population_mod < 0:
                city.population += population_mod
                self.message_buffer.append(str(population_mod * -1) + " people have died from hunger and thirst, Sultan.")
            if city.population < 1:
                city.population = 0
                city.economy = 0
                self.message_buffer.append("The city of " + city.name + " has died, Sultan.")
                self.game_over_flag = True

        # calc growth
        for city in self.local_player.cities:
            city_growth_percentage = 0
            for bldg in city.buildings:
                city.food += bldg.food_mod
                city.water += bldg.water_mod
                city.happiness += bldg.happiness_mod
                city.economy += bldg.economy_mod
                city_growth_percentage += bldg.population_growth_percent_mod
            growth_amount = int(city.population * (city_growth_percentage/100 + (city.population_growth_percent_base/100)))
            city.population += growth_amount
            self.message_buffer.append(str(growth_amount) + " babies were born in your city, Sultan.")

    def next_turn(self):
        self.month += self.months_per_turn
        if self.month >= 12:
            self.month = self.month % 12
            self.year += 1
        self.turn += 1
        self.random_encounter_flag = False

    def show_status(self):
        print("STATUS")

    def ProcessTurn(self):
        self.message_buffer.clear()
        if self.turn == self.max_turns:
            self.engine_running = False
            return
        self.process_players()
        self.next_turn()


    def game_loop(self):
        while self.engine_running:
            self.GetInput()
            self.ProcessTurn()
        self.end_game_process()

        # calc the player score


# define our clear function
def clear():
    # for windows
    os.system('cls' if os.name == 'nt' else 'clear')

clear()
game = GameEngine()
game.game_start()
