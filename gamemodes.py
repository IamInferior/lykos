# To add new game modes, rename this file to 'gamemodes.py' then add them in

from src.gamemodes import (GameMode, game_mode, reset_roles)
import src.settings as var
from src.utilities import *
from src.messages import messages
from src import events

####################################################################
# DO NOT EDIT ANYTHING ABOVE THIS LINE, ADD CUSTOM GAMEMODES BELOW #
####################################################################

@game_mode("mymode", minp=4, maxp=24, likelihood=5)
class MyMode(GameMode):
    """Example mode. This doesn't do anything special yet."""
    def __init__(self, arg=""):
        super().__init__(arg)
        # Put gamemode settings here

    def startup(self):
        # Register events here
        pass

    def teardown(self):
        # Unregister events here
        pass

@game_mode("dubslav", minp = 4, maxp = 20, likelihood = 4)
class dubslavMode(GameMode):
    def __init__(self, arg=""):
        super().__init__(arg)
        self.SHARPSHOOTER_CHANCE = 0.25
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

        self.ROLE_INDEX =         (   4   ,   5   ,   6   ,   7   ,   8   ,   9   ,  10   ,  11   ,  12   ,   13   ,  15   ,  17   ,  18   ,  20   )
        self.ROLE_GUIDE = reset_roles(self.ROLE_INDEX)
        self.ROLE_GUIDE.update({
              # village roles
              "oracle"          : (   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "harlot"          : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "shaman"          : (   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ),
              "vigilante"       : (   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ),
	            "hunter"          : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   ),
              "guardian angel"  : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ),
	            "village drunk"   : (   0   ,   0   ,   0   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ),
              # wolf roles
              "wolf"            : (   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   2   ,   1   ,   1   ,   1   ,   2   ,   3   ),
              "traitor"         : (   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "werecrow"        : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ),
              "wolf shaman"     : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "cultist"         : (   0   ,   0   ,   0   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   0   ),
	            "minion"          : (   0   ,   0   ,   0   ,   0   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ),
              # neutral roles
              "fool"            : (   0   ,   1   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ),
              "monster"         : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ),
	            "crazed shaman"   : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
	            "succubus"        : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   ),
              "wild child"      : (   0   ,   0   ,   0   ,   0   ,   1   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ),
              # templates
              "cursed villager" : (   0   ,   0   ,   1   ,   2   ,   2   ,   2   ,   2   ,   2   ,   2   ,   2   ,   2   ,   2   ,   3   ,   3   ),
              "gunner"          : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   2   ,   2   ),
	            "sharpshooter"    : (   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   0   ,   1   ,   1   ,   1   ,   1   ,   1   ,   1   )
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

