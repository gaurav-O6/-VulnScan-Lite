import SecurityScore from "./SecurityScore";
import FindingsSummary from "./FindingsSummary";
import FindingsList from "./FindingsList";


function Dashboard({ scan, onNewScan }) {


    if (!scan?.report) {

        return null;

    }


    const findings = scan.report.findings || [];



    function handleDownload() {

        const reportData = JSON.stringify(
            scan.report,
            null,
            2
        );


        const blob = new Blob(
            [reportData],
            {
                type:"application/json"
            }
        );


        const url = URL.createObjectURL(blob);


        const link = document.createElement("a");

        link.href = url;

        link.download = "vulnscan-report.json";

        link.click();


        URL.revokeObjectURL(url);

    }



    return (

        <section className="dashboard">


            <div className="dashboard-header">


                <div>


                    <h2>
                        Security Assessment Dashboard
                    </h2>


                    <p>
                        Passive vulnerability assessment report for the scanned target.
                    </p>


                </div>




                <div className="dashboard-status">


                    <span className="status-complete">

                        ● Scan Completed

                    </span>


                </div>


            </div>





            <div className="dashboard-actions">


                <button
                    className="report-action-button"
                    onClick={handleDownload}
                >

                    Download Report

                </button>




                {
                    onNewScan &&

                    <button
                        className="secondary-action-button"
                        onClick={onNewScan}
                    >

                        New Scan

                    </button>

                }


            </div>





            <div className="dashboard-top-grid">


                <div className="dashboard-left-column">


                    <div className="scan-meta-card">


                        <div>

                            <span>
                                Target
                            </span>


                            <strong>
                                {scan.target_url}
                            </strong>


                        </div>




                        <div>

                            <span>
                                Status
                            </span>


                            <strong className="status-complete">

                                Completed

                            </strong>


                        </div>




                        <div>

                            <span>
                                Security Score
                            </span>


                            <strong>
                                {scan.score}/100
                            </strong>


                        </div>


                    </div>





                    <FindingsSummary
                        findings={findings}
                    />


                </div>




                <div className="dashboard-right-column">


                    <SecurityScore
                        score={scan.score}
                        grade={scan.grade}
                    />


                </div>


            </div>





            <div className="dashboard-findings">


                <FindingsList
                    findings={findings}
                />


            </div>


        </section>

    );

}


export default Dashboard;