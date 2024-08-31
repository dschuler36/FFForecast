import type { Load } from '@sveltejs/kit';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;


async function getCurrentSeasonWeek() {
    const response = await fetch(`${API_BASE_URL}/api/current-season-week`);
    const responseData = await response.json();
    return responseData; 
}


async function getHalfPprPredictions(season: number, week: number) {
    const response = await fetch(`${API_BASE_URL}/api/predictions/half_ppr?season=${season}&week=${week}`);
    const responseData = await response.json();
    return responseData;
}


async function getFullPprPredictions(season: number, week: number) {
    const response = await fetch(`${API_BASE_URL}/api/predictions/full_ppr?season=${season}&week=${week}`);
    const responseData = await response.json();
    return responseData;
}


async function getDKDFSPredictions(season: number, week: number) {
    const response = await fetch(`${API_BASE_URL}/api/predictions/dk_dfs?season=${season}&week=${week}`);
    const responseData = await response.json();
    return responseData;
}

export const load: Load = async ({ parent }) => {
    try {
        const seasonWeek = await getCurrentSeasonWeek();
        // const season = seasonWeek.season;
        // const week = seasonWeek.week;
        const season = 2023;
        const week = 1;
        const halfPprPredictions = await getHalfPprPredictions(season, week);
        const fullPprPredictions = await getFullPprPredictions(season, week);
        const dkDFSPredictions = await getDKDFSPredictions(season, week);
        return {
            props: {
                season,
                week,
                halfPprPredictions, 
                fullPprPredictions,
                dkDFSPredictions
            }
        };
        } 
     catch (error) {
        console.error('Error fetching leagues:', error);
        return {
            status: 500,
            error: {
                message: 'Internal Server Error',
                details: error.message
            }
        };
    }
};