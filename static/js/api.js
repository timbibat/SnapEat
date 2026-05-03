/**
 * API Wrapper
 * Handles all communication between the frontend and Flask backend.
 */

const FoodAPI = {
    identify: async (data) => {
        const response = await fetch('/api/food/identify', {
            method: 'POST',
            body: data
        });
        return response.json();
    },
    
    getDetails: async (foodId) => {
        const response = await fetch(`/api/food/details/${foodId}`);
        return response.json();
    }
};
