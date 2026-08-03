import SecurityScore from "./SecurityScore";
import FindingsSummary from "./FindingsSummary";
import FindingsList from "./FindingsList";


function Dashboard({ scan, onNewScan }) {


    if (!scan?.report) {

        return null;

    }


    const findings = scan.report.findings || [];



    const severityCounts = {

        critical: findings.filter(
            (item) => item.severity?.toLowerCase() === "critical"
        ).length,

        high: findings.filter(
            (item) => item.severity?.toLowerCase() === "high"
        ).length,

        medium: findings.filter(
            (item) => item.severity?.toLowerCase() === "medium"
        ).length,

        low: findings.filter(
            (item) => item.severity?.toLowerCase() === "low"
        ).length

    };



    function handleDownload() {


        const reportData = JSON.stringify(
            scan.report,
            null,
            2
        );


        const blob = new Blob(
            [reportData],
            {
                type: "application/json"
            }
        );


        const url = URL.createObjectURL(blob);


        const link = document.createElement("a");


        link.href = url;

        link.download = "vulnscan-report.json";


        link.click();


        URL.revokeObjectURL(url);

    }





    function getRiskClass(level) {


        if (!level) {

            return "";

        }


        const value = level.toLowerCase();



        if (value === "low") {

            return "dashboard-risk-low";

        }


        if (value === "medium") {

            return "dashboard-risk-medium";

        }


        if (value === "high") {

            return "dashboard-risk-high";

        }


        return "dashboard-risk-critical";

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

                    <span>

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





            <SecurityScore

                score={scan.score}

                grade={scan.grade}

            />






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


                    <span className="meta-badge dashboard-status-completed">

                        Completed

                    </span>


                </div>





                <div>

                    <span>
                        Risk Level
                    </span>


                    <span
                        className={
                            `meta-badge ${getRiskClass(scan.risk_level)}`
                        }
                    >

                        {scan.risk_level}

                    </span>


                </div>





                <div>

                    <span>
                        Security Score
                    </span>


                    <strong>

                        {scan.score}/100

                    </strong>


                </div>





                <div>

                    <span>
                        Grade
                    </span>


                    <strong>

                        {scan.grade}

                    </strong>


                </div>





                <div>

                    <span>
                        Scan Duration
                    </span>


                    <strong>

                        {
                            scan.duration_seconds
                            ? `${scan.duration_seconds}s`
                            : "N/A"
                        }

                    </strong>


                </div>





                <div>

                    <span>
                        Total Findings
                    </span>


                    <strong>

                        {findings.length}

                    </strong>


                </div>





                <div>

                    <span>
                        Critical Issues
                    </span>


                    <strong>

                        {severityCounts.critical}

                    </strong>


                </div>





                <div>

                    <span>
                        High Risk
                    </span>


                    <strong>

                        {severityCounts.high}

                    </strong>


                </div>





                <div>

                    <span>
                        Medium Risk
                    </span>


                    <strong>

                        {severityCounts.medium}

                    </strong>


                </div>





                <div>

                    <span>
                        Low Risk
                    </span>


                    <strong>

                        {severityCounts.low}

                    </strong>


                </div>


            </div>







            <FindingsSummary

                findings={findings}

            />






            <div className="dashboard-findings">


                <FindingsList

                    findings={findings}

                />


            </div>


        </section>


    );


}


export default Dashboard;