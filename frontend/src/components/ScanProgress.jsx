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


        const value = status?.toLowerCase();


        if (value === "completed") {

            return "scan-status-completed";

        }


        if (value === "failed") {

            return "scan-status-failed";

        }


        return "scan-status-running";

    }







    function getStatusLabel(status) {


        const value = status?.toLowerCase();



        if (value === "completed") {

            return "Scan Completed";

        }


        if (value === "failed") {

            return "Scan Failed";

        }


        if (value === "queued") {

            return "Queued";

        }


        return "Scanning Website";

    }








    function getRiskLabel(score) {


        if (
            score === null ||
            score === undefined
        ) {

            return "--";

        }



        if (score >= 90) {

            return "Low";

        }



        if (score >= 70) {

            return "Medium";

        }



        if (score >= 50) {

            return "High";

        }



        return "Critical";

    }






    const status =
        scan.status?.toLowerCase();



    const progress =
        scan.progress ?? 0;



    const currentStage =
        scan.current_stage ?? "Initializing";





    const isScanning = [

        "queued",
        "running",
        "processing",
        "in_progress",
        "started"

    ].includes(status);






    return (

        <div

            className={
                `scan-card ${
                    status === "completed"
                    ? "scan-completed"
                    : ""
                }`
            }

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

                    className={
                        `scan-status-badge ${getStatusClass(status)}`
                    }

                >

                    {getStatusLabel(status)}

                </span>


            </div>







            {
                isScanning &&

                <>

                    <div className="scan-animation-bar">

                        <div
                            className="scan-animation-progress"
                        >

                        </div>

                    </div>



                    <div
                        className="scan-progress-info"
                    >

                        <strong>
                            {currentStage}
                        </strong>


                        <strong>
                            {progress}%
                        </strong>


                    </div>


                </>

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
                    status === "completed" &&

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






                        <div className="scan-info-box">

                            <span>
                                Risk Level
                            </span>


                            <strong>
                                {getRiskLabel(scan.score)}
                            </strong>

                        </div>






                        <div className="scan-info-box">

                            <span>
                                Scan Duration
                            </span>


                            <strong>

                                {
                                    scan.duration_seconds !== null &&
                                    scan.duration_seconds !== undefined

                                    ? `${Number(scan.duration_seconds).toFixed(1)}s`

                                    : "--"
                                }

                            </strong>

                        </div>






                        <div className="scan-info-box">

                            <span>
                                Findings
                            </span>


                            <strong>
                                {scan.report?.findings?.length ?? "--"}
                            </strong>

                        </div>


                    </>

                }








                {
                    status === "failed" &&

                    <div className="scan-error">

                        Scan failed while analyzing target.
                        Please verify the URL and try again.

                    </div>

                }



            </div>



        </div>

    );

}


export default ScanProgress;