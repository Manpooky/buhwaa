import {useQuery} from "@tanstack/react-query"

//This hook will re-fetch the upload results every 2 seconds until the upload is complete or fails
//It will also refetch in the background if the user navigates away from the page
//It will retry up to 3 times with an exponential backoff
export function useUploadResults( jobId: string, enabled: boolean = false) {
    const uploadQuery = useQuery({
        queryKey: ['upload', jobId],
        queryFn: async () => {
            const response = await fetch(`/api/upload/${jobId}`);
            if (!response.ok){
                throw new Error('Failed to fetch upload results');
            }
            return response.json();
        },
        enabled: enabled && !!jobId,
        refetchInterval: (data: any) => {
            if (data?.status === 'complete' || data?.status === 'error'){
                return false;
            }
            return 2000;
        },
        refetchIntervalInBackground: true,
        retry: 3,
        retryDelay: (attemptIndex: number) => Math.min(1000 * 2 ** attemptIndex, 30000)
    })

    return uploadQuery
}