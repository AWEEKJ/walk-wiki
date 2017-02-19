# -*- coding: utf-8 -*-
import json
import configparser
# planet_list = [1, 4, 5, 9, 12, 15, 20, 21, 22, 23, 25, 35, 45, 46, 50, 52, 53, 66, 69, 75, 81, 86, 87, 89, 101]


class Walkr():
    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read('game/settings.ini')

        self.language = parser['localization']['language']
        self.planets = list()
        self.satellites = list()

        self.wiki = self.get_wiki()

    def get_planet_list(self):
        with open('game/history.json') as f:
            history_dict = json.load(f)
            for history in history_dict['history']:
                self.planets.append(history['planet'])
            f.close()

    def get_wiki(self):
        if self.language == "en":
            with open('game/wiki/wiki_en.json') as f:
                data = json.load(f)
                f.close()
        elif self.language == "ko":
            with open('game/wiki/wiki_ko.json') as f:
                data = json.load(f)
                f.close()
        return data

    def get_satellite_list(self):
        for planet in self.planets:
            satellite = self.wiki['planet'][str(planet)]['acquired']
            self.satellites.append(satellite)
        self.satellites.sort()

    def find_best_match(self):
        match_list = list(set(self.planets).intersection(self.satellites))
        match_list.sort()

        if self.language == "en":
            print("\nThere is " + str(len(match_list)) + " best matches you have.\n")
            print("No".center(6) + "|"
                  + "Planet".center(20) + "|"
                  + "Satellite".center(30) + "|"
                  + "Boost".center(30) + "|")
            print('{:-<98}'.format(""))

            for match in match_list:
                planet = self.wiki["planet"][str(match)]
                satellite = self.wiki["satellite"][str(match)]

                info = ""
                info += str(match).center(6) + "|"
                info += planet['name'].center(20) + "|"
                info += satellite['name'].center(30) + "|"
                info += str(satellite.get('boost')).center(30) + "|"
                info += satellite['l2'].center(8)
                print(info)

        elif self.language == "ko":
            print("\n" + str(len(match_list)) + "개의 조합이 있습니다.\n")
            print("No".ljust(4) + "|  "
                  + "행성".ljust(15) + "\t|  "
                  + "위성".ljust(14) + "\t|  "
                  + "효과".ljust(13) + "\t|  ")
            print('{:-<90}'.format(""))

            for match in match_list:
                planet = self.wiki["planet"][str(match)]
                satellite = self.wiki["satellite"][str(match)]

                info = ""
                info += str(match).ljust(4) + "|  "
                info += planet['name'].ljust(15) + "\t|  "
                info += satellite['name'].ljust(14) + "\t|  "
                info += str(satellite.get('boost')).ljust(13) + "\t|  "
                info += satellite['l2'].ljust(8)
                print(info)

    def main(self):
        self.get_planet_list()
        self.get_satellite_list()
        self.find_best_match()

if __name__ == '__main__':
    walkr = Walkr()
    walkr.main()