import { useState } from "react";
import api from "../api/client";


function ScanForm({ onScanCreated }) {

    const [url, setUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    async function handleSubmit(e) {

        e.preventDefault();

        setError("");

        if (!url.trim()) {
            setError("Please enter a target URL.");
            return;
        }


        try {

            setLoading(true);


            const response = await api.post(
                "/scans",
                {
                    url: url.trim(),
                }
            );


            onScanCreated(response.data.scan_id);


        } catch (err) {

            console.error(err);

            setError(
                "Failed to create scan."
            );

        } finally {

            setLoading(false);

        }

    }



    return (

        <form
            className="scan-form"
            onSubmit={handleSubmit}
        >

            <input
                type="url"
                placeholder="https://example.com"
                value={url}
                onChange={
                    (e) => setUrl(e.target.value)
                }
            />


            <button
                type="submit"
                disabled={loading}
            >

                {
                    loading
                        ? "Starting..."
                        : "Start Scan"
                }

            </button>


            {
                error &&
                <p className="error">
                    {error}
                </p>
            }


        </form>

    );

}


export default ScanForm;
