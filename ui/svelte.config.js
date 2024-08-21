import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter()
	}

	// kit: {
	// 	adapter: adapter({
	// 	  out: '.svelte-kit/output/server',
	// 	  env: {
	// 		host: '0.0.0.0',
	// 		port: '$PORT'
	// 	  }
	// 	})
	//   }
	}
;

export default config;
