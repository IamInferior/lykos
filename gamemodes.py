# To add new game modes, rename this file to 'gamemodes.py' then add them in

from src.gamemodes import (GameMode, game_mode, reset_roles)
import src.settings as var
import random
from src.utilities import *
from src.messages import messages
from src import events

####################################################################
# DO NOT EDIT ANYTHING ABOVE THIS LINE, ADD CUSTOM GAMEMODES BELOW #
####################################################################

@game_mode("dubslav", minp = 4, maxp = 24, likelihood = 8)
class dubslavMode(GameMode):
    def __init__(self, arg=""):
        super().__init__(arg)
        self.SHARPSHOOTER_CHANCE = 1
                                              #    SHAMAN   , CRAZED SHAMAN , WOLF SHAMAN
        self.TOTEM_CHANCES = {       "death": (      0      ,       1       ,      0      ),
                                "protection": (      0      ,       1       ,      0      ),
                                   "silence": (      1      ,       1       ,      0      ),
                                 "revealing": (      4      ,       1       ,      0      ),
                               "desperation": (      0      ,       1       ,      0      ),
                                "impatience": (      0      ,       1       ,      0      ),
                                  "pacifism": (      1      ,       1       ,      0      ),
                                 "influence": (      1      ,       1       ,      0      ),
                                "narcolepsy": (      1      ,       1       ,      0      ),
                                  "exchange": (      0      ,       1       ,      0      ),
                               "lycanthropy": (      0      ,       1       ,      0      ),
                                      "luck": (      1      ,       1       ,      0      ),
                                "pestilence": (      3      ,       1       ,      0      ),
                               "retribution": (      1      ,       1       ,      0      ),
                              "misdirection": (      1      ,       1       ,      0      ),
                                    "deceit": (      0      ,       1       ,      0      ),
                             }

        # get default values for wolf shaman's chances
        for totem, (s, cs, ws) in self.TOTEM_CHANCES.items():
            self.TOTEM_CHANCES[totem] = (s, cs, var.TOTEM_CHANCES[totem][2])

        self.ROLE_INDEX =         (   4   ,   5   ,   6   ,   7   ,   8   ,   9   ,  10   ,  11   ,  12   ,   13   ,  15   ,  17   ,  18   ,  20  ,   22   )
        self.ROLE_GUIDE = reset_roles(self.ROLE_INDEX)
        self.ROLE_GUIDE.update({
              # village roles
              "oracle"          : (   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "harlot"          : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "shaman"          : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ),
              "vigilante"       : (   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ),
	            "hunter"          : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "guardian angel"  : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ),
	            "village drunk"   : (   0   ,   0   ,   0   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ),
              # wolf roles
              "wolf"            : (   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   ),
              "traitor"         : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "werecrow"        : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ),
              "wolf cub"        : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "wolf shaman"     : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "cultist"         : (   0   ,   0   ,   0   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ),
	            "minion"          : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ),
              # neutral roles
              "fool"            : (   0   ,   1   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ),
              "monster"         : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ),
	            "crazed shaman"   : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "jester"          : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ),
              "clone"           : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
	            "succubus"        : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   ,   2   ),
              "wild child"      : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ),
              "lycan"           : (   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              # templates
              "cursed villager" : (   0   ,   0   ,   1   ,   2   ,   2   ,   2   ,   2   ,   2   ,   2   ,   2   ,   3   ,   3   ,   3   ,   3   ,   3   ),
              "gunner"          : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   2   ,   2   ,   2   ),
	            "sharpshooter"    : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   )
              })

    def transition_night_begin(self, evt, cli, var):
        if var.FIRST_NIGHT:
            # ensure shaman gets protection totem on the first night
            var.TOTEM_CHANCES["protection"] = (100, 1, 0)
        else:
            var.TOTEM_CHANCES["protection"] = (0, 1, 0)

@game_mode("ppd", minp = 4, maxp = 21, likelihood = 0)
class PpdMode(GameMode):
    """PPD game mode with guardian angel"""
    def __init__(self, arg=""):
        super().__init__(arg)
        self.ABSTAIN_ENABLED = False
        self.ROLE_INDEX =         (   4   ,   6   ,   8   ,  10   ,  12   ,  15   ,  17   ,  18   ,  20   )
        self.ROLE_GUIDE = reset_roles(self.ROLE_INDEX)
        self.ROLE_GUIDE.update({# village roles
              "seer"            : (   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "village drunk"   : (   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "harlot"          : (   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "guardian angel"          : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "bodyguard"       : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ),
              "detective"       : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              # wolf roles
              "wolf"            : (   1   ,   1   ,   1   ,   2   ,   2   ,   3   ,   3   ,   3   ,   4   ),
              "traitor"         : (   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "werecrow"        : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              # templates
              "cursed villager" : (   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   ,   2   ),
              "gunner"          : (   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   )
              })

@game_mode("edgy", minp = 4, maxp = 20, likelihood = 1)
class EdgyMode(GameMode):
    """pssh nothing personnel kid"""
    def __init__(self, arg=""):
        super().__init__(arg)
        
        self.ABSTAIN_ENABLED = False
        self.SHARPSHOOTER_CHANCE = 1
        self.ROLE_INDEX =         (   4   ,   6   ,   7   ,   8   ,   9   ,  10   ,  11   ,  12   ,  14   ,  16   ,  18   )
        self.ROLE_GUIDE = reset_roles(self.ROLE_INDEX)
        self.ROLE_GUIDE.update({# village roles
              "mad scientist"   : (   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "harlot"          : (   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "prophet"         : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "vigilante"       : (   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "oracle"          : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ),
              # wolf roles
              "fallen angel"    : (   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   ,   3   ),
              "traitor"         : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   2   ,   2   ,   2   ),
              "werecrow"        : (   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              # neutral roles
              "demoniac"        : (   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "turncoat"        : (   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "crazed shaman"   : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "vengeful ghost"  : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ),
              # templates
              "cursed villager" : (   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "gunner"          : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ),
              "sharpshooter"    : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ),
              "assassin"        : (   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   )
              })

    def startup(self):
        events.add_listener("transition_day_resolve", self.edgyday)

    def teardown(self):
        events.remove_listener("transition_day_resolve", self.edgyday)

    def edgyday(self, evt, var, victims):
        evt.data["message"].append(random.choice(["\npssh nothing personnel kid\n", 
          "\ni'll stop wearing black when they invent a darker color MOM",
          "\nthe devil whispered to me you'll never wtihstand the storm\n\nBUT I AM THE STORM\n",
          "\nMy name is not important. What is important is what I'm going to do... I just fuckin' hate this world\n",
          "\ni can be yuor angel or yur demon\n",
          "\ni have two sides nicest guy you'll ever meet and TWISTED FUCKING PSYCHOPATH\n",
          "\nim a fucking dark triad man don't mess with me\n",
          "\nYou laugh at me because I'm different, I laugh at you because you're all the same.\n",
          "\nI didn't ask to be born...but now I'm asking to die\n",
          "\nits hard to answer teh question whats wrong when nothing is right. my silents is words for my pain.\n",
          "\nTO BE FAIR YOU HAVE TO HAVE\n",
          "\ntown is full of fucking sheeple and i am the wolf come to make my harvest\n",
          "\nCan't save you all. Don't want to.\n",
          "\neverybody either loves you or hates you\n",
          "\ndon't get confused between my personality and my attitude. my personality is who i am, my attitude depends on who you are\n",
          "\nhope springs eternal but only fools drink from it.\n",
          "\nPitter, patter, the rain starts to drop. While the water may fill up the hole on the road, it will never fill up the hole of one's heart.\n",
          "\nMy name is Uchiha Sasuke, there are lot's of things I dislike and I don't really like anything.\n",
          "\nit wasn't me who was wrong. it was the world.\n",
          "\nyou laugh at me because i'm different. i laugh cos ur all the same\n",
          "\njust stay out of my way. i'll do this alone if I have to.\n",
          "\nthe werewolves arent the real monster here\n",
          "\nthis is my curse... i am the death come for you\n",
          "\nlmao friends you think friends wont betray you for a quick buck and fuck sonaive\n",
          "\ni'm not a pyschopath im a high functioning psychopath\n",
          "\nmY hEaD iS a DaRk PlAcE\n"]))


@game_mode("awesome", minp = 4, maxp = 21, likelihood = 0)
class AwesomeMode(GameMode):
    """Awesome mode by Madeleine."""
    def __init__(self, arg=""):
        super().__init__(arg)
        self.ABSTAIN_ENABLED = False
        self.ROLE_INDEX =         (   4   ,   6   ,   7   ,   8   ,   9   ,  10   ,  11   ,  12   ,   13   ,  15   ,  17   ,  18   ,  20   )
        self.ROLE_GUIDE = reset_roles(self.ROLE_INDEX)
        self.ROLE_GUIDE.update({# village roles
              "seer"            : (   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "village drunk"   : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "harlot"          : (   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "guardian angel"  : (   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "detective"       : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              # wolf roles
              "wolf"            : (   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   ,   2   ,   2   ,   2   ,   2   ,   3   ),
              "traitor"         : (   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "werecrow"        : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
	      "wolf cub"	: (   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "cultist"		: (   0   ,   0   ,   1   ,   0   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   0   ),
	      # neutral roles
	      "vengeful ghost"  : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
	      "monster"		: (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              # templates
              "cursed villager" : (   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   ,   2   ),
              "gunner"          : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
	      "mayor"           : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   )
              })

@game_mode("perfect", minp = 4, maxp = 24, likelihood = 4)
class perfectMode(GameMode):
    def __init__(self, arg=""):
        super().__init__(arg)
        self.SHARPSHOOTER_CHANCE = 1
                                              #    SHAMAN   , CRAZED SHAMAN , WOLF SHAMAN
        self.TOTEM_CHANCES = {       "death": (      3      ,       1       ,      0      ),
                                "protection": (      8      ,       1       ,      0      ),
                                   "silence": (      2      ,       1       ,      0      ),
                                 "revealing": (      0      ,       1       ,      0      ),
                               "desperation": (      0      ,       1       ,      0      ),
                                "impatience": (      1      ,       1       ,      0      ),
                                  "pacifism": (      1      ,       1       ,      0      ),
                                 "influence": (      2      ,       1       ,      0      ),
                                "narcolepsy": (      0      ,       1       ,      0      ),
                                  "exchange": (      0      ,       1       ,      0      ),
                               "lycanthropy": (      0      ,       1       ,      0      ),
                                      "luck": (      0      ,       1       ,      0      ),
                                "pestilence": (      1      ,       1       ,      0      ),
                               "retribution": (      1      ,       1       ,      0      ),
                              "misdirection": (      0      ,       1       ,      0      ),
                                    "deceit": (      0      ,       1       ,      0      ),
                             }
        
        # get default values for wolf shaman's chances
        for totem, (s, cs, ws) in self.TOTEM_CHANCES.items():
            self.TOTEM_CHANCES[totem] = (s, cs, var.TOTEM_CHANCES[totem][2])
        
        self.ROLE_INDEX =         (   4   ,   6   ,   7   ,   8   ,   9   ,  10   ,  11   ,  12   ,   13   ,  15   ,  17   ,  18   ,  20   )
        self.ROLE_GUIDE = reset_roles(self.ROLE_INDEX)
        self.ROLE_GUIDE.update({
              # village roles
              "seer"            : (   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "harlot"          : (   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "shaman" 		: (   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "detective"       : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
	      "matchmaker"      : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              # wolf roles
              "wolf"            : (   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   ,   2   ,   2   ,   3   ),
              "traitor"         : (   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "werecrow"        : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
	      "wolf cub"	: (   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "cultist"		: (   0   ,   0   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   0   ),
	      # neutral roles
	      "clone"        : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "monster"		: (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              # templates
              "cursed villager" : (   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   ,   2   ),
              "gunner"          : (   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   )
              })

