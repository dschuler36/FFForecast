import type { Load } from '@sveltejs/kit';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;


async function getCompletedWeeks() {
    const response = await fetch(`${API_BASE_URL}/api/accuracy/completed-weeks`);
    const responseData = await response.json();
    return responseData; 
}


export const load: Load = async ({ parent }) => {
    try {
        const weeks = await getCompletedWeeks();
        return {
            props: {
                weeks
            }
        };
        } 
     catch (error) {
        console.error('Error fetching completed weeks:', error);
        return {
            status: 500,
            error: {
                message: 'Internal Server Error',
                details: error.message
            }
        };
    }
};