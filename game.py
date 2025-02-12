from character import Character
import os
import json

class CharacterRound():
    
    def __init__(self, scenario: str, objectives: list[str], secret_objectives: list[str]):
        self.scenario = scenario
        self.objectives = objectives,
        self.secret_objectives = secret_objectives

class Round():

    def __init__(self, name, number, details=None):
        self.name = name
        self.number = str(number)
        self.details = details or dict()

    def add_character_round(self, character: Character, scenario: str, objectives: list[str], secret_objectives: list[str]):

        self.details[character.name] = CharacterRound(
            scenario=scenario,
            objectives=objectives,
            secret_objectives=secret_objectives
        )

    def save(self, game_slug):

        outobj = dict(
            name = self.name,
            number = self.number,
            details ={
                x: y.__dict__ for x, y in self.details.items()
            }
        )

        with open(f"games/{game_slug}/rounds/{self.number}.json","w") as outfile:
            outfile.write(json.dumps(outobj))


class Game():

    def __init__(self):
        self.characters = dict()
        self.rounds = list()
        self.name = ""
        self.slug = ""
        self.description = ""

    def load(self, slug):
        self.slug=slug
        character_files=os.listdir(f'games/{self.slug}/characters')
        round_files=os.listdir(f'games/{self.slug}/rounds')

        info_file  = open(f"games/{self.slug}/info.json", "r").read()
        info_json = json.loads(info_file)
        self.name = info_json["name"]
        self.description = info_json["description"]

        for cfile in character_files:
            character_name = cfile.replace(".json","")
            self.characters[character_name] = Character(game=self.slug, name=character_name)
        
        for rfile in round_files:
            round_json = json.loads(open(f'games/{self.slug}/rounds/{rfile}',"r").read())
            self.rounds.append(
                Round(
                    name=round_json["name"],
                    number=round_json["number"],
                    details={
                        x: CharacterRound(**y) for x, y in round_json["details"].items()
                    }  
                )    
            )

    def save(self):
        for character_name, character in self.characters.items():
            character.save()

        for round in self.rounds:
            round.save(self.slug)


        with open(f"games/{self.slug}/info.json", "w") as outfile:
            info = dict(
                name = self.name,
                slug=self.slug,
                description = self.description
            )
            
            outfile.write(json.dumps(info))
        
    def add_character(self, character: Character):
        character.game=self.slug
        self.characters[character.name] = character
        character.save()

    def get_character(self, character_name, round_number):
        return self.characters[character_name]
    
    def add_round(self, name, number):
        new_round = Round(
            name=name,
            number=number
        )

        self.rounds.append(new_round)

        return new_round
