# -*- coding: utf-8 -*-
import json
import configparser
from datetime import datetime


class Walkr():

    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read('game/settings.ini')

        self.language = parser['localization']['language']
        self.planets = list()
        self.satellites = list()

        self.wiki = self.get_wiki()

    @staticmethod
    def read_history():
        with open('game/history.json') as f:
            data = {int(key): value for key, value in json.load(f).items()}
            return data

    @staticmethod
    def write_history(data):
        with open('game/history.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_history(self, new_planet_list):
        if len(new_planet_list) == 0:
            return
        else:
            self.get_planet_list()
            history = self.read_history()
            today = datetime.now().strftime('%Y-%m-%d')

            for planet in new_planet_list:
                if planet in self.planets:
                    print("You already have " + str(planet))
                    continue
                else:
                    history[int(planet)] = today

            self.write_history(history)

    def get_planet_list(self):
        history = self.read_history()
        for item in history.items():
            self.planets.append(item[0])
        self.planets.sort()

    def get_wiki(self):
        if self.language == "en":
            with open('game/wiki/wiki_en.json') as f:
                data = json.load(f)
        elif self.language == "ko":
            with open('game/wiki/wiki_ko.json') as f:
                data = json.load(f)
        return data

    def get_satellite_list(self):
        for planet in self.planets:
            satellite = self.wiki['planet'][str(planet)]['acquired']
            self.satellites.append(satellite)
        self.satellites.sort()

    def find_best_match(self):

        self.get_planet_list()
        self.get_satellite_list()

        bests = list(set(self.planets).intersection(self.satellites))
        bests.sort()

        result = list()

        for planet_num in bests:
            planet = self.wiki["planet"][str(planet_num)]
            satellite = self.wiki["satellite"][str(planet_num)]

            info = dict()
            info['no'] = planet_num
            info['planet'] = planet['name']
            info['satellite'] = satellite['name']
            info['boost_name'] = satellite.get('boost')
            info['boost_level'] = 2
            info['boost_amount'] = satellite['l2']
            result.append(info)

        self.write_result(result)

        return result

    @staticmethod
    def read_result():
        with open('game/result.json') as f:
            data = json.load(f)
            return data

    @staticmethod
    def write_result(data):
        with open('game/result.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def print_result(self):
        self.find_best_match()
        result = self.read_result()

        print("\nThere is " + str(len(result)) + " best matches you have.\n")
        print("No".center(6) + "|"
              + "Planet".center(20) + "|"
              + "Satellite".center(30) + "|"
              + "Boost".center(30) + "|")
        print('{:-<98}'.format(""))

        for item in result:
            info = ""
            info += str(item['no']).center(6) + "|"
            info += item['planet'].center(20) + "|"
            info += item['satellite'].center(30) + "|"
            info += str(item['boost_name']).center(30) + "|"
            info += item['boost_amount'].center(8)
            print(info)

    def main(self):
        self.add_history([])
        self.print_result()

if __name__ == '__main__':
    walkr = Walkr()
    walkr.main()