import { useState } from "react";
import api from "../api/client";


function ScanForm({ onScanCreated }) {


    const [url, setUrl] = useState("");

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");




    function validateUrl(value) {


        let formattedUrl = value.trim();


        if (!formattedUrl) {

            return {
                valid:false,
                message:"Please enter a target URL."
            };

        }



        if (
            !formattedUrl.startsWith("http://") &&
            !formattedUrl.startsWith("https://")
        ) {

            formattedUrl = "https://" + formattedUrl;

        }



        try {

            const parsed = new URL(formattedUrl);


            if (
                !parsed.hostname.includes(".")
            ) {

                return {
                    valid:false,
                    message:"Please enter a valid website URL."
                };

            }


            return {
                valid:true,
                url:formattedUrl
            };


        } catch {


            return {
                valid:false,
                message:"Please enter a valid website URL."
            };

        }

    }





    async function handleSubmit(e) {


        e.preventDefault();


        setError("");



        const validation = validateUrl(url);



        if (!validation.valid) {

            setError(validation.message);

            return;

        }





        try {


            setLoading(true);



            const response = await api.post(
                "/scans",
                {
                    url: validation.url,
                }
            );



            onScanCreated(
                response.data.scan_id
            );



            setUrl("");



        } catch (err) {


            console.error(
                "Scan creation error:",
                err
            );


            setError(
                "Failed to create scan. Please try again."
            );


        } finally {


            setLoading(false);


        }


    }





    function handleChange(e) {


        setUrl(e.target.value);


        if (error) {

            setError("");

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

                onChange={handleChange}

                disabled={loading}

                aria-label="Target website URL"

            />




            <button

                type="submit"

                disabled={loading}

            >

                {
                    loading
                    ? "Initializing Scan..."
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