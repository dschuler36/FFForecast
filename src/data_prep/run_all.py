from src.data_prep import plays_agg, player_influence, weekly_rosters


if __name__ == '__main__':
    run_id = '20240809'
    print('Running plays_agg...')
    plays_agg.main(run_id)
    print('Running weekly_rosters...')
    weekly_rosters.main(run_id)
    print('Running player_influence...')
    player_influence.main(run_id)