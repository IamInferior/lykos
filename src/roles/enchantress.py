import re
import random
import itertools
import math
from collections import defaultdict

import botconfig
import src.settings as var
from src.utilities import *
from src import channels, users, debuglog, errlog, plog
from src.functions import get_players, get_all_players, get_main_role, get_reveal_role, get_target
from src.containers import UserList, UserSet, UserDict, DefaultUserDict
from src.decorators import command, event_listener
from src.messages import messages
from src.events import Event

from src.roles import harlot
from src.roles import succubus

ENTRANCED = UserSet() # type: Set[users.User]
ENTRANCED_DYING = UserSet() # type: Set[users.User]
VISITED = UserDict() # type: Dict[users.User, users.User]
PASSED = UserSet() # type: Set[users.User]
ALL_SUCC_IDLE = True
ENTRANCED_ALIVE_NUM = 0

@command("visit", chan=False, pm=True, playing=True, silenced=True, phases=("night",), roles=("enchantress",))
def hvisit(var, wrapper, message):
    global ENTRANCED_ALIVE_NUM
    """Entrance a player, converting them to your team."""
    if VISITED.get(wrapper.source):
        wrapper.send(messages["succubus_already_visited"].format(VISITED[wrapper.source]))
        return

    target = get_target(var, wrapper, re.split(" +", message)[0], not_self_message="succubus_not_self")
    if not target:
        return

    evt = Event("targeted_command", {"target": target, "misdirection": True, "exchange": True})
    if not evt.dispatch(var, wrapper.source, target):
        return
    target = evt.data["target"]

    VISITED[wrapper.source] = target
    PASSED.discard(wrapper.source)
    succ_num = len(get_all_players(("enchantress",)))

    succ_capped = ENTRANCED_ALIVE_NUM >= succ_num * 2

    if target in get_all_players(("succubus",)) or target in get_all_players(("harlot",)) or target in get_all_players(("enchantress",)):
        if VISITED.get(target):
            wrapper.send(messages["succubus_notathome"].format(VISITED[wrapper.source]))
            return
        if harlot.VISITED.get(target):
            wrapper.send(messages["succubus_notathome"].format(VISITED[wrapper.source]))
            return
        if succubus.VISITED.get(target):
            wrapper.send(messages["succubus_notathome"].format(VISITED[wrapper.source]))
            return

    if target not in get_all_players(("enchantress",)) and ENTRANCED_ALIVE_NUM < succ_num * 2:
        ENTRANCED.add(target)
        wrapper.send(messages["succubus_target_success"].format(target))
    else:
        wrapper.send(messages["harlot_success"].format(target))

    if wrapper.source is not target:
        if target not in get_all_players(("enchantress",)) and ENTRANCED_ALIVE_NUM < succ_num * 2:
            target.send(messages["notify_succubus_target"].format(wrapper.source))
            ENTRANCED_ALIVE_NUM = ENTRANCED_ALIVE_NUM + 1
        else:
            target.send(messages["harlot_success"].format(wrapper.source))

        revt = Event("succubus_visit", {})
        if succ_capped:
            revt = Event("harlot_visit", {})

        revt.dispatch(var, wrapper.source, target)

    debuglog("{0} (enchantress) VISIT: {1} ({2})".format(wrapper.source, target, get_main_role(target)))

@command("pass", chan=False, pm=True, playing=True, silenced=True, phases=("night",), roles=("enchantress",))
def pass_cmd(var, wrapper, message):
    """Do not entrance someone tonight."""
    if VISITED.get(wrapper.source):
        wrapper.send(messages["succubus_already_visited"].format(VISITED[wrapper.source]))
        return

    PASSED.add(wrapper.source)
    wrapper.send(messages["succubus_pass"])
    debuglog("{0} (enchantress) PASS".format(wrapper.source))

@event_listener("harlot_visit")
def on_harlot_visit(evt, var, harlot, victim):
    if victim in get_all_players(("enchantress",)) and ENTRANCED_ALIVE_NUM < succ_num * 2:
        harlot.send(messages["notify_succubus_target"].format(victim))
        victim.send(messages["succubus_harlot_success"].format(harlot))
        ENTRANCED.add(harlot)
        ENTRANCED_ALIVE_NUM = ENTRANCED_ALIVE_NUM + 1

@event_listener("get_random_totem_targets")
def on_get_random_totem_targets(evt, var, shaman):
    if shaman in ENTRANCED:
        for enchantress in get_all_players(("enchantress",)):
            if enchantress in evt.data["targets"]:
                evt.data["targets"].remove(enchantress)

@event_listener("chk_decision")
def on_chk_decision(evt, cli, var):
    for votee, voters in evt.data["votelist"].items():
        if votee in get_all_players(("enchantress",)): # FIXME
            for vtr in ENTRANCED:
                if vtr.nick in voters:
                    evt.data["numvotes"][votee] -= evt.data["weights"][votee][vtr.nick]
                    evt.data["weights"][votee][vtr.nick] = 0

def _kill_entranced_voters(var, votelist, not_lynching, votee):
    if not {p.nick for p in get_all_players(("enchantress",))} & (set(itertools.chain(*votelist.values())) | not_lynching): # FIXME
        # none of the succubi voted (or there aren't any succubi), so short-circuit
        return
    # kill off everyone entranced that did not follow one of the succubi's votes or abstain
    # unless a enchantress successfully voted the target, then people that didn't follow are spared
    for x in ENTRANCED:
        if x.nick not in var.DEAD:
            ENTRANCED_DYING.add(x)

    for other_votee, other_voters in votelist.items():
        if {p.nick for p in get_all_players(("enchantress",))} & set(other_voters): # FIXME
            if votee == other_votee:
                ENTRANCED_DYING.clear()
                return

            for x in set(ENTRANCED_DYING):
                if x.nick in other_voters:
                    ENTRANCED_DYING.remove(x)

    if {p.nick for p in get_all_players(("enchantress",))} & not_lynching: # FIXME
        if votee is None:
            ENTRANCED_DYING.clear()
            return

        for x in set(ENTRANCED_DYING):
            if x.nick in not_lynching:
                ENTRANCED_DYING.remove(x)

@event_listener("chk_decision_lynch", priority=5)
def on_chk_decision_lynch(evt, cli, var):
    # a different event may override the original votee, but people voting along with enchantress
    # won't necessarily know that, so base whether or not they risk death on the person originally voted
    _kill_entranced_voters(var, evt.params.votelist, evt.params.not_lynching, evt.params.original_votee)

@event_listener("chk_decision_abstain")
def on_chk_decision_abstain(evt, var, not_lynching):
    _kill_entranced_voters(var, evt.params.votelist, not_lynching, None)

# entranced logic should run after team wins have already been determined (aka run last)
@event_listener("player_win", priority=6)
def on_player_win(evt, var, user, role, winner, survived):
    if user in ENTRANCED:
        evt.data["special"].append("entranced")
        if winner != "fae":
            evt.data["won"] = False
            evt.data["iwon"] = False
        else:
            evt.data["won"] = True
            evt.data["iwon"] = survived
    if role == "enchantress":
        if winner == "fae":
            evt.data["won"] = True
            evt.data["iwon"] = True
        else:
            evt.data["won"] = False
            evt.data["iwon"] = False

@event_listener("chk_win", priority=2)
def on_chk_win(evt, var, rolemap, mainroles, lpl, lwolves, lrealwolves):
    lsuccubi = len(rolemap.get("enchantress", ()))
    lentranced = len([x for x in ENTRANCED if x.nick not in var.DEAD])
    if lsuccubi and var.PHASE == "day" and lpl - lsuccubi == lentranced:
        evt.data["winner"] = "fae"
        evt.data["message"] = messages["succubus_win"].format(plural("faerie", lsuccubi), plural("has", lsuccubi), plural("master's", lsuccubi))

@event_listener("can_exchange")
def on_can_exchange(evt, var, actor, target):
    if actor in get_all_players(("enchantress",)) or target in get_all_players(("enchantress",)):
        evt.prevent_default = True
        evt.stop_processing = True

@event_listener("del_player")
def on_del_player(evt, var, user, mainrole, allroles, death_triggers):
    global ALL_SUCC_IDLE
    global ENTRANCED_ALIVE_NUM

    entranced_alive = ENTRANCED.difference(evt.params.deadlist).intersection(evt.data["pl"])
    ENTRANCED_ALIVE_NUM = len(entranced_alive)

    if "enchantress" not in allroles:
        return

    if user in VISITED:
        # if it's night, also unentrance the person they visited
        if var.PHASE == "night" and var.GAMEPHASE == "night":
            if VISITED[user] in ENTRANCED:
                ENTRANCED.discard(VISITED[user])
                ENTRANCED_DYING.discard(VISITED[user])
                VISITED[user].send(messages["entranced_revert_win"])
        del VISITED[user]

    # if all succubi are dead, one of two things happen:
    # 1. if all succubi idled out (every last one of them), un-entrance people
    # 2. otherwise, kill all entranced people immediately, they still remain entranced (and therefore lose)
    # death_triggers is False for an idle-out, so we use that to determine which it is
    if death_triggers:
        ALL_SUCC_IDLE = False
    if not get_all_players(("enchantress",)):
        if ALL_SUCC_IDLE:
            while ENTRANCED:
                e = ENTRANCED.pop()
                e.send(messages["entranced_revert_win"])
        elif entranced_alive:
            msg = []
            # Run in two loops so we can play the message for everyone dying at once before we actually
            # kill any of them off (if we killed off first, the message order would be wrong wrt death chains)
            comma = ""
            if var.ROLE_REVEAL in ("on", "team"):
                comma = ","
            for e in entranced_alive:
                if var.ROLE_REVEAL in ("on", "team"):
                    role = get_reveal_role(e)
                    an = "n" if role.startswith(("a", "e", "i", "o", "u")) else ""
                    msg.append("\u0002{0}\u0002, a{1} \u0002{2}\u0002".format(e, an, role))
                else:
                    msg.append("\u0002{0}\u0002".format(e))
            if len(msg) == 1:
                channels.Main.send(messages["enchantress_die_kill"].format(msg[0] + comma))
            elif len(msg) == 2:
                channels.Main.send(messages["enchantress_die_kill"].format(msg[0] + comma + " and " + msg[1] + comma))
            else:
                channels.Main.send(messages["enchantress_die_kill"].format(", ".join(msg[:-1]) + ", and " + msg[-1] + comma))
            for e in entranced_alive:
                # to ensure we do not double-kill someone, notify all child deaths that we'll be
                # killing off everyone else that is entranced so they don't need to bother
                dlc = list(evt.params.deadlist)
                dlc.extend(entranced_alive - {e})
                debuglog("{0} (enchantress) enchantress DEATH KILL: {1} ({2})".format(user, e, get_main_role(e)))
                evt.params.del_player(e, end_game=False, killer_role="enchantress",
                    deadlist=dlc, original=evt.params.original, ismain=False)
                evt.data["pl"] = evt.params.refresh_pl(evt.data["pl"])
        ENTRANCED_DYING.clear()

@event_listener("transition_day_resolve", priority=1)
def on_transition_day_resolve(evt, var, victim):
    if victim in get_all_players(("enchantress",)) and VISITED.get(victim) and victim not in evt.data["dead"] and victim in evt.data["onlybywolves"]:
        # TODO: check if this is necessary for enchantress, it's to prevent a message playing if alpha bites
        # a harlot that is visiting a wolf, since the bite succeeds in that case.
        if victim not in evt.data["bitten"]:
            evt.data["message"].append(messages["target_not_home"])
            evt.data["novictmsg"] = False
        evt.stop_processing = True
        evt.prevent_default = True

@event_listener("transition_day_resolve_end", priority=1)
def on_transition_day_resolve_end(evt, var, victims):
    for victim in victims + evt.data["bitten"]:
        if victim in evt.data["dead"] and victim in VISITED.values() and (victim in evt.data["bywolves"] or victim in evt.data["bitten"]):
            for enchantress in VISITED:
                if VISITED[enchantress] is victim and enchantress not in evt.data["bitten"] and enchantress not in evt.data["dead"]:
                    if var.ROLE_REVEAL in ("on", "team"):
                        evt.data["message"].append(messages["visited_victim"].format(enchantress, get_reveal_role(enchantress)))
                    else:
                        evt.data["message"].append(messages["visited_victim_noreveal"].format(enchantress))
                    evt.data["bywolves"].add(enchantress)
                    evt.data["onlybywolves"].add(enchantress)
                    evt.data["dead"].append(enchantress)

@event_listener("transition_day_resolve_end", priority=3)
def on_transition_day_resolve_end3(evt, var, victims):
    for succ in get_all_players(("enchantress",)):
        if VISITED.get(succ) in get_players(var.WOLF_ROLES) and succ not in evt.data["dead"] and succ not in evt.data["bitten"]:
            if(VISITED.get(succ) not in ENTRANCED):
                evt.data["message"].append(messages["enchantress_visited_wolf"].format(succ))
                evt.data["bywolves"].add(succ)
                evt.data["onlybywolves"].add(succ)
                evt.data["dead"].append(succ)

@event_listener("night_acted")
def on_night_acted(evt, var, target, spy):
    if VISITED.get(target):
        evt.data["acted"] = True

@event_listener("chk_nightdone")
def on_chk_nightdone(evt, var):
    evt.data["actedcount"] += len(VISITED) + len(PASSED)
    evt.data["nightroles"].extend(get_all_players(("enchantress",)))

@event_listener("transition_night_end", priority=2)
def on_transition_night_end(evt, var):
    succubi = get_all_players(("enchantress",))
    for enchantress in succubi:
        pl = get_players()
        random.shuffle(pl)
        pl.remove(enchantress)
        to_send = "enchantress_notify"
        succ = []
        for p in pl:
            if p in succubi:
                succ.append("{0} (enchantress)".format(p))
            else:
                succ.append(p.nick)
        enchantress.send(messages[to_send], "Players: " + ", ".join(succ), sep="\n")

@event_listener("begin_day")
def on_begin_day(evt, var):
    VISITED.clear()
    ENTRANCED_DYING.clear()
    PASSED.clear()

@event_listener("transition_day", priority=2)
def on_transition_day(evt, var):
    for v in ENTRANCED_DYING:
        var.DYING.add(v) # indicate that the death bypasses protections
        evt.data["victims"].append(v)
        evt.data["onlybywolves"].discard(v)
        # we do not add to killers as retribution totem should not work on entranced not following enchantress

@event_listener("get_special")
def on_get_special(evt, var):
    evt.data["win_stealers"].update(get_players(("enchantress",)))

@event_listener("vg_kill")
def on_vg_kill(evt, var, ghost, target):
    if ghost in ENTRANCED:
        evt.data["pl"] -= get_all_players(("enchantress",))

@event_listener("swap_player")
def on_swap(evt, var, old_user, user):
    if old_user in ENTRANCED:
        ENTRANCED.remove(old_user)
        ENTRANCED.add(user)
    if old_user in ENTRANCED_DYING:
        ENTRANCED_DYING.remove(old_user)
        ENTRANCED_DYING.add(user)

    for enchantress, target in set(VISITED.items()):
        if old_user is enchantress:
            VISITED[user] = VISITED.pop(enchantress)
        if old_user is target:
            VISITED[enchantress] = user

    if old_user in PASSED:
        PASSED.remove(old_user)
        PASSED.add(user)

@event_listener("reset")
def on_reset(evt, var):
    global ALL_SUCC_IDLE
    ALL_SUCC_IDLE = True
    ENTRANCED.clear()
    ENTRANCED_DYING.clear()
    VISITED.clear()
    PASSED.clear()

@event_listener("revealroles")
def on_revealroles(evt, var, wrapper):
    if ENTRANCED:
        evt.data["output"].append("\u0002entranced players\u0002: {0}".format(", ".join(p.nick for p in ENTRANCED)))

    if ENTRANCED_DYING:
        evt.data["output"].append("\u0002dying entranced players\u0002: {0}".format(", ".join(p.nick for p in ENTRANCED_DYING)))

# vim: set sw=4 expandtab:
