<script lang="ts">
    import { fade } from 'svelte/transition';
  
    export let playerStats: any[]; // Type this properly based on your actual data structure
  
    let showDetailedStats = false;
  
    function formatNumber(num: number): string {
      return num.toFixed(2);
    }
  

    // Function to calculate the difference and return a class for color coding
    function getDiffClass(diff: number): string {
      if (diff > 0) return "text-green-600";
      if (diff < 0) return "text-red-600";
      return "text-gray-600";
    }
  </script>

<div class="flex justify-center my-4">
    <label class="label cursor-pointer">
      <span class="label-text mr-2">Show detailed stats</span>
      <input type="checkbox" class="toggle toggle-primary" bind:checked={showDetailedStats} />
    </label>
  </div>
  
  <div class="overflow-x-auto">
    <table class="table table-zebra w-full">
      <thead>
        <tr>
          <th>Player Name</th>
          <th>Position</th>
          <th>Opponent</th>
          <th>Predicted Points</th>
          <th>Actual Points</th>
          <th>Difference</th>
        </tr>
      </thead>
      <tbody>
        {#each playerStats as player}
          <tr>
            <td>{player.player_name}</td>
            <td>{player.position}</td>
            <td>{player.opponent}</td>
            <td>{formatNumber(player.fantasy_points)}</td>
            <td>{formatNumber(player.fantasy_points_actual)}</td>
            <td class={getDiffClass(player.fantasy_points_diff)}>
              {formatNumber(player.fantasy_points_diff)}
            </td>
          </tr>
          {#if showDetailedStats}
            <tr transition:fade>
              <td colspan="6">
                <p class="text-sm italic text-gray-600 mb-2">
                  Format: prediction / actual (difference)
                </p>
                <div class="grid grid-cols-3 gap-4 p-4 bg-base-200 rounded-lg">
                  <div>
                    <h4 class="font-bold">Passing</h4>
                    <p>Yards: {formatNumber(player.passing_yards)} / {player.passing_yards_actual} ({formatNumber(player.passing_yards_diff)})</p>
                    <p>TDs: {formatNumber(player.passing_tds)} / {player.passing_tds_actual} ({formatNumber(player.passing_tds_diff)})</p>
                    <p>INTs: {formatNumber(player.interceptions)} / {player.interceptions_actual} ({formatNumber(player.interceptions_diff)})</p>
                  </div>
                  <div>
                    <h4 class="font-bold">Rushing</h4>
                    <p>Yards: {formatNumber(player.rushing_yards)} / {player.rushing_yards_actual} ({formatNumber(player.rushing_yards_diff)})</p>
                    <p>TDs: {formatNumber(player.rushing_tds)} / {player.rushing_tds_actual} ({formatNumber(player.rushing_tds_diff)})</p>
                  </div>
                  <div>
                    <h4 class="font-bold">Receiving</h4>
                    <p>Yards: {formatNumber(player.receiving_yards)} / {player.receiving_yards_actual} ({formatNumber(player.receiving_yards_diff)})</p>
                    <p>TDs: {formatNumber(player.receiving_tds)} / {player.receiving_tds_actual} ({formatNumber(player.receiving_tds_diff)})</p>
                    <p>Receptions: {formatNumber(player.receptions)} / {player.receptions_actual} ({formatNumber(player.receptions_diff)})</p>
                  </div>
                </div>
              </td>
            </tr>
          {/if}
        {/each}
      </tbody>
    </table>
  </div>
  