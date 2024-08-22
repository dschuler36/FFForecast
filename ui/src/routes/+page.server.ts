import type { Load } from '@sveltejs/kit';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function getHalfPprPredictions(season: number, week: number) {
    const response = await fetch(`${API_BASE_URL}/api/predictions/half_ppr?season=${season}&week=${week}`);
    const responseData = await response.json();
    return responseData;
}

export const load: Load = async ({ parent }) => {
    try {
        const halfPprPredictions = await getHalfPprPredictions(2024, 1);
        return {
            props: {
                halfPprPredictions
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