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
            halfPprPredictions: Array<any>
        } 
    };
    let players: PlayerStats[] = data.props.halfPprPredictions;
    let selectedPosition: string = 'All';
    function filterPlayers(position: string) {
        selectedPosition = position;
    }

  $: filteredPlayers = selectedPosition === 'All'
    ? players
    : selectedPosition === 'Flex'
    ? players.filter(player => ['RB', 'WR', 'TE'].includes(player.base.position))
    : players.filter(player => player.base.position === selectedPosition);

</script>


<main class="container mx-auto p-4">
  <h1 class="text-3xl font-bold mb-4">NumbersFF - Predictions</h1>
  <h2 class="text-3 font-bold mb-4">2023 Week 1</h2>
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
  
  <div class="overflow-x-auto">
    <table class="table table-zebra w-full">
      <thead>
        <tr>
          <th>Player Name</th>
          <th>Position</th>
          <th>Team</th>
          <th>Opponent</th>
          <th>Week</th>
          <th>Passing Yards</th>
          <th>Passing TDs</th>
          <th>Rushing Yards</th>
          <th>Rushing TDs</th>
          <th>Receptions</th>
          <th>Receiving Yards</th>
          <th>Receiving TDs</th>
          <th>Fantasy Points</th>
        </tr>
      </thead>
      <tbody>
        {#each filteredPlayers as player}
          <tr>
            <td>{player.base.player_name}</td>
            <td>{player.base.position}</td>
            <td>{player.base.team}</td>
            <td>{player.base.opponent}</td>
            <td>{player.base.week}</td>
            <td>{player.base.passing_yards.toFixed(2)}</td>
            <td>{player.base.passing_tds.toFixed(2)}</td>
            <td>{player.base.rushing_yards.toFixed(2)}</td>
            <td>{player.base.rushing_tds.toFixed(2)}</td>
            <td>{player.base.receptions.toFixed(2)}</td>
            <td>{player.base.receiving_yards.toFixed(2)}</td>
            <td>{player.base.receiving_tds.toFixed(2)}</td>
            <td>{player.fantasy_points.toFixed(2)}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</main>