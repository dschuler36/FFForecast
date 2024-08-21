import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: vitePreprocess(),

    kit: {
        adapter: adapter({
            // default options are shown
            out: 'build',
            precompress: false,
            env: {
                port: process.env.PORT || 3000,
                host: '0.0.0.0'
            }
        })
    }
	}
};

export default config;
