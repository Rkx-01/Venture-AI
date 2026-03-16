/**
 * Retrieves the API base URL from the environment.
 * Validates that the necessary environment variable is set.
 * 
 * @returns The base URL of the backend API as a string.
 * @throws Error if the environment variable is not defined.
 */
export function getApiBaseUrl(): string {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;

    if (!apiUrl) {
        throw new Error(
            "Missing critical environment variable: NEXT_PUBLIC_API_URL is not defined. " +
            "Please ensure it is set in your .env.local file."
        );
    }

    return apiUrl;
}
