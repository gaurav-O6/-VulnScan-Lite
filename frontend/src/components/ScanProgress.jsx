function ScanProgress({ scan }) {

    if (!scan) {

        return (

            <div className="scan-card scan-empty-state">

                <div className="scan-empty-icon">

                    🛡️

                </div>

                <h2>

                    Ready to Scan

                </h2>

                <p>

                    Enter a website URL above to begin a passive security assessment.
                    Your live scan status and results will appear here.

                </p>

                <div className="scan-empty-hint">

                    No active scan

                </div>

            </div>

        );

    }


    function getStatusClass(status) {

        if (status === "completed") {

            return "scan-status-completed";

        }

        if (status === "failed") {

            return "scan-status-failed";

        }

        return "scan-status-running";

    }



    function getStatusLabel(status) {

        if (status === "completed") {

            return "Scan Completed";

        }

        if (status === "failed") {

            return "Scan Failed";

        }

        return "Scanning Website";

    }



    return (

        <div
            className={`scan-card ${
                scan.status === "completed"
                    ? "scan-completed"
                    : ""
            }`}
        >

            <div className="scan-card-header">

                <div className="scan-title">

                    <h2>
                        Scan Status
                    </h2>

                    <p>
                        Live security assessment progress.
                    </p>

                </div>

                <span
                    className={`scan-status-badge ${getStatusClass(scan.status)}`}
                >

                    {getStatusLabel(scan.status)}

                </span>

            </div>


            {
                scan.status === "running" &&

                <div className="scan-animation-bar">

                    <div className="scan-animation-progress"></div>

                </div>

            }


            <div className="scan-info-grid">

                <div className="scan-info-box">

                    <span>

                        Target

                    </span>

                    <strong>

                        {scan.target_url}

                    </strong>

                </div>


                <div className="scan-info-box">

                    <span>

                        Current Status

                    </span>

                    <strong>

                        {scan.status}

                    </strong>

                </div>


                {
                    scan.status === "completed" &&

                    <>

                        <div className="scan-info-box">

                            <span>

                                Security Score

                            </span>

                            <strong>

                                {scan.score}/100

                            </strong>

                        </div>


                        <div className="scan-info-box">

                            <span>

                                Grade

                            </span>

                            <strong>

                                {scan.grade}

                            </strong>

                        </div>

                    </>

                }


                {
                    scan.status === "running" &&

                    <div className="scan-progress-message">

                        <span className="pulse-dot"></span>

                        Analyzing security configuration and vulnerabilities...

                    </div>

                }


                {
                    scan.status === "failed" &&

                    <div className="scan-error">

                        Scan failed. Please try again.

                    </div>

                }

            </div>

        </div>

    );

}

export default ScanProgress;