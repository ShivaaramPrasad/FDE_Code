import { useState, useEffect } from "react";

export const usePaginatedFetch = <T,>(url: string, fetchLimit: number, pageSize: number) => {
    const [data, setData] = useState<T[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);

    useEffect(() => {
        setLoading(true);
        setError(null);
        setPage(1);
        fetch(`${url}?limit=${fetchLimit}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch data");
                }
                return response.json();
            })
            .then((data: T[]) => {
                setData(data);
            })
            .catch((err: Error) => {
                setError(err.message);
            })
            .finally(() => {
                setLoading(false);
            });
    }, [url, fetchLimit]);

    const totalPages = Math.max(1, Math.ceil(data.length / pageSize));
    const pageData = data.slice((page - 1) * pageSize, page * pageSize);

    return { pageData, loading, error, page, totalPages, setPage };
}
