<svelte:head>
  <title>About | FFForecast</title>
  <meta name="description" content="About FFForecast" />
</svelte:head>

<div class="container mx-auto px-4 py-8">
  <h1 class="text-5xl font-bold mb-8 text-center">About FFForecast</h1>
  
  <div class="card bg-base-200 shadow-xl mb-8">
    <div class="card-body">
      <p class="text-lg">
        Welcome to our fully automated NFL stats and fantasy football prediction site. We're on a quest to create the most accurate NFL predictions available, relying solely on data and machine learning without any manual human intervention.
      </p>
      <p class="text-lg mt-4">
        Our goal is to provide you with unbiased, data-driven insights that can give you an edge in your fantasy football leagues and NFL analysis.
      </p>
    </div>
  </div>

  <div class="grid md:grid-cols-2 gap-8">
    <div class="card bg-base-200 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-2xl mb-4">How It Works</h2>
        <p>
          Our prediction model uses advanced machine learning algorithms to analyze vast amounts of NFL data. We consider factors such as player performance, team statistics, historical trends, and more to generate our predictions.
        </p>
        <p class="mt-4">
          By removing human bias and relying entirely on data, we aim to provide the most objective and accurate predictions possible.
        </p>
      </div>
    </div>

    <div class="card bg-base-200 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-2xl mb-4">Our Commitment to Accuracy</h2>
        <p>
          We continuously refine and improve our algorithms to enhance prediction accuracy. Our system learns from each game, adjusting its models to account for new trends and patterns in the NFL landscape.
        </p>
      </div>
    </div>
  </div>

  <div class="card bg-base-200 shadow-xl mt-8">
    <div class="card-body">
      <h2 class="card-title text-2xl mb-4">Data Attribution</h2>
      <p>
        We proudly use data and packages from <a href="https://github.com/nflverse" class="link link-primary">nflverse</a>, which follows the Creative Commons Public License. We are grateful for their contribution to the NFL data community.
      </p>
      <p class="text-sm mt-4">
        nflverse data is licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/" class="link link-primary">CC BY-SA 4.0</a>
      </p>
    </div>
  </div>
</div>