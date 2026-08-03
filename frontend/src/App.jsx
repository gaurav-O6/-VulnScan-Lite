import { useEffect, useState } from "react";

import api from "./api/client";

import ScanForm from "./components/ScanForm";
import ScanProgress from "./components/ScanProgress";
import Dashboard from "./components/Dashboard";

import History from "./pages/History";

import "./App.css";


function App() {


    const [page, setPage] = useState("scanner");

    const [scanId, setScanId] = useState(null);

    const [scan, setScan] = useState(null);



    function handleScanCreated(id) {

        setScanId(id);

        setScan(null);

        setPage("scanner");

    }




    function handleSelectScan(id) {

        setScanId(id);

        setPage("scanner");

    }





    function handleNewScan() {

        setScanId(null);

        setScan(null);

        setPage("scanner");

    }






    useEffect(() => {


        if (!scanId) {

            return;

        }


        let interval;


        async function fetchScan() {

            try {


                const response = await api.get(
                    `/scans/${scanId}`
                );


                setScan(response.data);



                if (

                    response.data.status === "completed" ||

                    response.data.status === "failed"

                ) {

                    if (interval) {

                        clearInterval(interval);

                    }

                }


            } catch (error) {


                console.error(
                    "Polling error:",
                    error
                );


            }

        }



        fetchScan();



        interval = setInterval(
            fetchScan,
            2000
        );



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
                    Automated Website Security Assessment Platform
                </p>


            </header>







            <div className="passive-warning">


                <span className="warning-icon">
                    ⚠
                </span>


                <div>

                    <strong>
                        Passive Security Assessment Only
                    </strong>


                    <p>
                        Only scan websites you own.
                        VulnScan Lite performs passive analysis
                        and does not execute aggressive attacks.
                    </p>

                </div>


            </div>









            <nav className="navigation">


                <button

                    className={
                        page === "scanner"
                            ? "active-nav"
                            : ""
                    }

                    onClick={() => setPage("scanner")}

                >

                    Scanner

                </button>






                <button

                    className={
                        page === "history"
                            ? "active-nav"
                            : ""
                    }

                    onClick={() => setPage("history")}

                >

                    History

                </button>


            </nav>









            <main>


                {
                    page === "scanner"

                    ?


                    <>


                        <section className="scanner-panel">


                            <div className="section-header">


                                <div>


                                    <h2>
                                        Start Security Scan
                                    </h2>


                                    <p>
                                        Scan a website and generate a security assessment report.
                                    </p>


                                </div>


                            </div>






                            <ScanForm

                                onScanCreated={handleScanCreated}

                            />


                        </section>







                        <ScanProgress

                            scan={scan}

                        />








                        {
                            scan?.report &&

                            <Dashboard

                                scan={scan}

                                onNewScan={handleNewScan}

                            />

                        }


                    </>


                    :


                    <History

                        onSelectScan={handleSelectScan}

                    />

                }


            </main>









            <footer className="app-footer">


                <div>


                    <strong>
                        VulnScan Lite
                    </strong>


                    <p>
                        Automated passive website security assessment platform.
                    </p>


                </div>








                <div className="footer-right">


                    <span>
                        Built for cybersecurity learning & assessment
                    </span>


                    <span>
                        © {new Date().getFullYear()} VulnScan Lite
                    </span>


                </div>


            </footer>


        </div>

    );

}


export default App;