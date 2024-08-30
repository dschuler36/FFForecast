<script lang="ts">
    export let metrics: {
      MAE: number;
      MSE: number;
      RMSE: number;
      R_squared: number;
      season: number;
      week: number;
    };
  
    const formatNumber = (num: number) => num.toFixed(2);
  </script>
  
  <div class="flex flex-wrap gap-4 justify-center items-stretch mb-8">
    <div class="card bg-base-100 shadow-xl tooltip" data-tip="Mean Absolute Error: Average magnitude of prediction errors. Lower is better.">
      <div class="card-body">
        <h2 class="card-title">MAE</h2>
        <p class="text-2xl font-bold">{formatNumber(metrics.MAE)}</p>
        <p class="text-sm text-gray-500">Points off on average</p>
      </div>
    </div>
    
    <div class="card bg-base-100 shadow-xl tooltip" data-tip="Root Mean Square Error: Average magnitude of prediction errors, with higher weight on larger errors. Lower is better.">
      <div class="card-body">
        <h2 class="card-title">RMSE</h2>
        <p class="text-2xl font-bold">{formatNumber(metrics.RMSE)}</p>
        <p class="text-sm text-gray-500">Weighted average error</p>
      </div>
    </div>
    
    <div class="card bg-base-100 shadow-xl tooltip" data-tip="R-squared: Proportion of variance in the actual scores that is predictable from the model. Closer to 1 is better.">
      <div class="card-body">
        <h2 class="card-title">R²</h2>
        <p class="text-2xl font-bold">{formatNumber(metrics.R_squared)}</p>
        <p class="text-sm text-gray-500">Model accuracy (0-1)</p>
      </div>
    </div>
    
    <div class="card bg-base-100 shadow-xl tooltip" data-tip="Mean Squared Error: Average of the squares of the errors. Used in calculating RMSE.">
      <div class="card-body">
        <h2 class="card-title">MSE</h2>
        <p class="text-2xl font-bold">{formatNumber(metrics.MSE)}</p>
        <p class="text-sm text-gray-500">Squared error average</p>
      </div>
    </div>
    
  </div>