<script lang="ts">
    import { createEventDispatcher } from 'svelte';
  
    export let completedWeeks: { season: number; week: number }[] = [];
    
    const dispatch = createEventDispatcher();
  
    let selectedWeek: { season: number; week: number } | null = null;
  
    function handleSelect() {
      if (selectedWeek) {
        dispatch('weekSelected', selectedWeek);
      }
    }
  </script>
  
  <div class="form-control w-full max-w-xs">
    <label for="week-select" class="label">
      <span class="label-text">Select a completed week</span>
    </label>
    <select 
      id="week-select"
      class="select select-bordered"
      bind:value={selectedWeek}
      on:change={handleSelect}
    >
      <option value={null} disabled selected>Choose a week</option>
      {#each completedWeeks as week (week.season + '-' + week.week)}
        <option value={week}>
          Season {week.season} - Week {week.week}
        </option>
      {/each}
    </select>
  </div>
  