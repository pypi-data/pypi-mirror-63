from AoE2ScenarioParser.objects.aoe2_object import AoE2Object


class PlayerObject(AoE2Object):
    def __init__(self,
                 player_number,
                 active,
                 human,
                 civilization,
                 gold,
                 wood,
                 food,
                 stone,
                 color,
                 starting_age,
                 pop_limit
                 ):

        super().__init__(locals())
