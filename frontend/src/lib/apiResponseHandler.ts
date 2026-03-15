export interface ApiResponse<T> {
    success: boolean;
    data: T | null;
    error: {
        message: string;
        status: number;
        details?: any;
    } | null;
}

/**
 * Normalizes a successful backend response into a predictable frontend structure.
 */
export const handleSuccessResponse = <T>(data: T): ApiResponse<T> => {
    return {
        success: true,
        data,
        error: null,
    };
};

/**
 * Normalizes a failed backend response into a predictable frontend error structure.
 * Ensures consistent error messaging across the application.
 */
export const handleErrorResponse = (error: any): ApiResponse<null> => {
    let message = "An unexpected error occurred. Please try again.";
    let status = 500;
    let details = null;

    if (error?.response) {
        
        status = error.response.status;
        message = error.response.data?.detail || error.response.data?.message || `API Error: ${status}`;
        details = error.response.data; 
    } else if (error?.request) {
        
        message = "No response received from the server. Please check your connection.";
        status = 0;
    } else if (error instanceof Error) {
        
        message = error.message;
    } else if (typeof error === "string") {
        
        message = error;
    }

    
    if (process.env.NODE_ENV === "development") {
        console.error(`[API Error] ${status}:`, message, error);
    }

    return {
        success: false,
        data: null,
        error: {
            message,
            status,
            details,
        },
    };
};
