import { useEffect, useState } from "react";

import api from "./api/client";

import ScanForm from "./components/ScanForm";
import ScanProgress from "./components/ScanProgress";

import SecurityScore from "./components/SecurityScore";
import FindingsSummary from "./components/FindingsSummary";
import FindingsList from "./components/FindingsList";

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






            <nav className="navigation">


                <button

                    onClick={() => setPage("scanner")}

                >

                    Scanner

                </button>




                <button

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


                        <ScanForm

                            onScanCreated={handleScanCreated}

                        />





                        <ScanProgress

                            scan={scan}

                        />







                        {
                            scan?.report &&


                            <>


                                <SecurityScore

                                    scan={scan}

                                />





                                <FindingsSummary

                                    findings={
                                        scan.report.findings
                                    }

                                />





                                <FindingsList

                                    findings={
                                        scan.report.findings
                                    }

                                />



                            </>


                        }



                    </>


                    :


                    <History

                        onSelectScan={handleSelectScan}

                    />

                }



            </main>



        </div>

    );

}



export default App;