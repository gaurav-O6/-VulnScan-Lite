import { useEffect, useState } from "react";

import api from "./api/client";

import ScanForm from "./components/ScanForm";
import ScanProgress from "./components/ScanProgress";

import "./App.css";


function App() {

    const [scanId, setScanId] = useState(null);

    const [scan, setScan] = useState(null);



    function handleScanCreated(id) {

        setScanId(id);

    }



    useEffect(() => {


        if (!scanId) {
            return;
        }


        const interval = setInterval(async () => {


            try {

                const response = await api.get(
                    `/scans/${scanId}`
                );


                setScan(response.data);


                if (
                    response.data.status === "completed" ||
                    response.data.status === "failed"
                ) {

                    clearInterval(interval);

                }


            } catch (error) {

                console.error(
                    "Polling error:",
                    error
                );

            }


        }, 2000);



        return () => {

            clearInterval(interval);

        };


    }, [scanId]);




    return (

        <div className="app">


            <header className="header">

                <h1>
                    VulnScan Lite
                </h1>

                <p>
                    Automated Website Security Scanner
                </p>

            </header>



            <main>


                <ScanForm
                    onScanCreated={handleScanCreated}
                />



                <ScanProgress
                    scan={scan}
                />


                {
                    scan?.report &&

                    <div className="report-card">

                        <h2>
                            Security Report
                        </h2>


                        <p>
                            Findings:
                            {" "}
                            {
                                scan.report.findings?.length || 0
                            }
                        </p>


                        <p>
                            Scan completed successfully.
                        </p>


                    </div>

                }


            </main>


        </div>

    );

}


export default App;
