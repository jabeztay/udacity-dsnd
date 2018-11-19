from secret import api_key
import helper as h
import pandas as pd
from chicken_dinner.pubgapi import PUBG


def main():
    shard = 'pc-sea'
    pubg = PUBG(api_key, shard)
    samples = h.get_samples(pubg)
    total = len(samples)
    count = 0

    for match in samples:
        # getting telemetry data fails on some matches
        try:
            info, drops, weapons, damage, kills = h.clean_match(pubg, match)
            files = ['drops', 'weapons', 'damage', 'kills']

            for idx, df in enumerate([drops, weapons, damage, kills]):
                df['match_id'] = match
                df.to_csv('data/{}.csv'.format(files[idx]),
                          header=False,
                          index=False,
                          mode='a',
                          encoding='utf-8')

            info.to_csv('data/matches.csv',
                        header=False,
                        index=False,
                        mode='a',

                        encoding='utf-8')
            count += 1

        except:
            total -= 1
            print('Error with match {}'.format(match))

        print('{}/{} matches done'.format(str(count), str(total)))


if __name__ == '__main__':
    main()
