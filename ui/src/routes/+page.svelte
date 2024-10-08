<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    interface PlayerStats {
        base: {
            season: number;
            rushing_yards: number;
            opponent: string;
            week: number;
            rushing_tds: number;
            player_name: string;
            player_id: string;
            rushing_2pt_conversions: number;
            team: string;
            passing_yards: number;
            receptions: number;
            position: string;
            passing_tds: number;
            receiving_yards: number;
            interceptions: number;
            receiving_tds: number;
            fumbles: number;
            receiving_2pt_conversions: number;
            passing_2pt_conversions: number;
        };
        fantasy_points: number;
    }

    export let data: {
        props: { 
            season: number,
            week: number,
            halfPprPredictions: Array<any>,
            fullPprPredictions: Array<any>,
            dkDFSPredictions: Array<any>
        } 
    };
    let season: number = data.props.season;
    let week: number = data.props.week;
    let halfPprRankings: PlayerStats[] = data.props.halfPprPredictions;
    let fullPprRankings: PlayerStats[] = data.props.fullPprPredictions;
    let dkDFSRankings: PlayerStats[] = data.props.dkDFSPredictions;

    $: predictionsReady = halfPprRankings.length > 0 || fullPprRankings.length > 0 || dkDFSRankings.length > 0;

    let selectedPosition: string = 'All';
    let scoringType: 'half' | 'full' | 'dkDFS' = 'half';

    function filterPlayers(position: string) {
        selectedPosition = position;
    }

    function switchScoringType(type: 'half' | 'full' | 'dkDFS') {
        scoringType = type;
    }

    let showExpandedStats = false;

    function toggleExpandedStats() {
        showExpandedStats = !showExpandedStats;
    }

    $: filteredPlayers = (
        scoringType === 'half' ? halfPprRankings :
        scoringType === 'full' ? fullPprRankings :
        dkDFSRankings
    ).filter(player => 
        selectedPosition === 'All' ? true :
        selectedPosition === 'Flex' ? ['RB', 'WR', 'TE'].includes(player.base.position) :
        player.base.position === selectedPosition
    );
</script>

<main class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Predictions</h1>
    <h2 class="text-3 font-bold mb-4">{season} Week {week}</h2>

    {#if predictionsReady}
        <div class="mb-4">
            <div class="btn-group">
                <button class="btn btn-sm" class:btn-active={scoringType === 'half'} on:click={() => switchScoringType('half')}>Half PPR</button>
                <button class="btn btn-sm" class:btn-active={scoringType === 'full'} on:click={() => switchScoringType('full')}>Full PPR</button>
                <button class="btn btn-sm" class:btn-active={scoringType === 'dkDFS'} on:click={() => switchScoringType('dkDFS')}>DK DFS</button>
            </div>
        </div>
        <div class="mb-4">
            <div class="btn-group">
                <button class="btn btn-sm" class:btn-active={selectedPosition === 'All'} on:click={() => filterPlayers('All')}>All</button>
                <button class="btn btn-sm" class:btn-active={selectedPosition === 'QB'} on:click={() => filterPlayers('QB')}>QB</button>
                <button class="btn btn-sm" class:btn-active={selectedPosition === 'RB'} on:click={() => filterPlayers('RB')}>RB</button>
                <button class="btn btn-sm" class:btn-active={selectedPosition === 'WR'} on:click={() => filterPlayers('WR')}>WR</button>
                <button class="btn btn-sm" class:btn-active={selectedPosition === 'TE'} on:click={() => filterPlayers('TE')}>TE</button>
                <button class="btn btn-sm" class:btn-active={selectedPosition === 'Flex'} on:click={() => filterPlayers('Flex')}>Flex</button>
            </div>
        </div>
        <div class="mb-4">
            <button class="btn btn-sm" on:click={toggleExpandedStats}>
                {showExpandedStats ? 'Hide' : 'Show'} More Stats
            </button>
        </div>

        <div class="overflow-x-auto">
            <table class="table table-zebra w-full">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Position</th>
                        <th>Team</th>
                        <th>Opponent</th>
                        <th>Week</th>
                        {#if showExpandedStats}
                            <th>Passing Yards</th>
                            <th>Passing TDs</th>
                            <th>Rushing Yards</th>
                            <th>Rushing TDs</th>
                            <th>Receptions</th>
                            <th>Receiving Yards</th>
                            <th>Receiving TDs</th>
                        {/if}
                        <th>Fantasy Points</th>
                    </tr>
                </thead>
                <tbody>
                    {#each filteredPlayers as player, index}
                        <tr>
                            <td>{index + 1}</td>
                            <td>{player.base.player_name}</td>
                            <td>{player.base.position}</td>
                            <td>{player.base.team}</td>
                            <td>{player.base.opponent}</td>
                            <td>{player.base.week}</td>
                            {#if showExpandedStats}
                                <td>{player.base.passing_yards.toFixed(2)}</td>
                                <td>{player.base.passing_tds.toFixed(2)}</td>
                                <td>{player.base.rushing_yards.toFixed(2)}</td>
                                <td>{player.base.rushing_tds.toFixed(2)}</td>
                                <td>{player.base.receptions.toFixed(2)}</td>
                                <td>{player.base.receiving_yards.toFixed(2)}</td>
                                <td>{player.base.receiving_tds.toFixed(2)}</td>
                            {/if}
                            <td>{player.fantasy_points.toFixed(2)}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {:else}
        <p class="text-xl text-center mt-8">Predictions not yet ready for {season} Week {week}. Check back in a bit.</p>
    {/if}
</main>