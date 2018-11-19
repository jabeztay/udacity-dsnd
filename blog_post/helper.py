from chicken_dinner.pubgapi import PUBG
import pandas as pd


def get_samples(pubg):
    '''Takes a PUBG object with shard, and returns sample matches'''
    samples = pubg.samples().data
    matches = samples['relationships']['matches']['data']
    matches = [match['id'] for match in matches]

    return matches


def game_phase(tele_event):
    '''Returns game phase of an event'''
    return tele_event['common']['is_game']


def get_location(tele_event_character):
    '''Returns location of a character, pass in tele_event['character']
    or ['killer'], ['victim'], ['attacker']'''
    return tele_event_character['location'].to_dict()


def get_item(tele_event):
    '''Returns item id'''
    return tele_event['item']['item_id']


def get_picked_weapons(tele_data):
    '''Returns DataFrame of weapons picked'''
    items_picked = tele_data.filter_by('log_item_pickup')
    weapons_picked = [item for item in items_picked \
                      if item['item']['category'] == 'Weapon']
    weapons = []

    for weapon in weapons_picked:
        weapons.append([game_phase(weapon), \
                        get_item(weapon), \
                        get_location(weapon['character'])])

    return pd.DataFrame(weapons)


def get_drop_location(tele_data):
    '''Returns DataFrame of drop locations'''
    items_unequipped = tele_data.filter_by('log_item_unequip')
    parachutes_unequipped = [unequip for unequip in items_unequipped \
                             if 'Parachute' in get_item(unequip)]
    drop_locations = []

    for drop in parachutes_unequipped:
        drop_locations.append([game_phase(drop), \
                               get_location(drop['character'])])

    return pd.DataFrame(drop_locations)


def get_damage_info(tele_data):
    '''Returns DataFrame of damage instances'''
    instances = tele_data.filter_by('log_player_take_damage')
    damage_events = []

    for event in instances:
        phase = game_phase(event)
        victim_loc = get_location(event['victim'])
        # blue zone, drowning, following, has no attacker
        try:
            attacker_loc = get_location(event['attacker'])
        except:
            attacker_loc = victim_loc
        damage = event['damage']
        damage_causer = event['damage_causer_name']
        damage_reason = event['damage_reason']
        damage_category = event['damage_type_category']

        damage_events.append([phase, \
                              attacker_loc, \
                              victim_loc, \
                              damage, \
                              damage_causer, \
                              damage_reason, \
                              damage_category])

    return pd.DataFrame(damage_events)


def get_kill_info(tele_data):
    '''Returns DataFrame of kill instances'''
    instances = tele_data.filter_by('log_player_kill')
    kills = []

    for event in instances:
        phase = game_phase(event)
        victim_loc = get_location(event['victim'])
        # blue zone, drowning, falling has no killer
        try:
            killer_loc = get_location(event['killer'])
        except:
            killer_loc = victim_loc
        damage_causer = event['damage_causer_name']
        damage_reason = event['damage_reason']
        damage_category = event['damage_type_category']
        distance = event['distance']

        kills.append([phase, \
                      killer_loc, \
                      victim_loc, \
                      damage_causer, \
                      damage_reason, \
                      damage_category, \
                      distance])

    return pd.DataFrame(kills)


def get_match_info(match_data, tele_data):
    '''Takes match and tele data and returns basic match info'''
    return pd.DataFrame([match_data.id, \
                      match_data.shard, \
                      match_data.game_mode, \
                      tele_data.started(), \
                      tele_data.map_name(), \
                      tele_data.match_length()]).T


def clean_match(pubg, match_id):
    '''Takes a PUBG object and match_id, returns match data'''
    match_data = pubg.match(match_id)
    tele_data = match_data.get_telemetry()

    match_info = get_match_info(match_data, tele_data)
    drop_locations = get_drop_location(tele_data)
    picked_weapons = get_picked_weapons(tele_data)
    damage_instances = get_damage_info(tele_data)
    kill_instances = get_kill_info(tele_data)

    return match_info, \
           drop_locations, \
           picked_weapons, \
           damage_instances, \
           kill_instances
