<script lang="ts">
import WeekSelector from '$lib/components/WeekSelector.svelte';
import OverallMetrics from '$lib/components/OverallMetrics.svelte';
import PlayerStatsTable from '$lib/components/PlayerStatsTable.svelte';
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
export let data: {
        props: { 
            weeks: Array<any>
        } 
    };
    let completedWeeks: { season: number; week: number }[] = [];
    completedWeeks = data.props.weeks;

    let overallMetrics: {
        MAE: number;
        MSE: number;
        RMSE: number;
        R_squared: number;
    } | null = null;

    let playerStats: any[] = []; // Type this properly based on your actual data structure


    async function handleWeekSelected(event: CustomEvent<{ season: number; week: number }>) {
        const selectedWeek = event.detail;
        console.log(selectedWeek);
        
        // Fetch overall accuracy metrics
        overallMetrics = await fetch(`${API_BASE_URL}/api/accuracy/metrics?season=${selectedWeek.season}&week=${selectedWeek.week}`).then(res => res.json());
        console.log(overallMetrics);
        
        // Fetch detailed player metrics
        playerStats = await fetch(`${API_BASE_URL}/api/accuracy/diffs?season=${selectedWeek.season}&week=${selectedWeek.week}`).then(res => res.json());
    // TODO: Update your component state with the fetched data
  }

</script>

<WeekSelector {completedWeeks} on:weekSelected={handleWeekSelected} />

{#if overallMetrics}
  <OverallMetrics metrics={overallMetrics} />
{/if}

{#if playerStats.length > 0}
  <PlayerStatsTable {playerStats} />
{/if}