import { useEffect, useState } from "react";

import api, { downloadPDFReport } from "../api/client";
import "../../styles/history.css";


function History({ onSelectScan }) {


    const [scans, setScans] = useState([]);

    const [loading, setLoading] = useState(true);

    const [deleting, setDeleting] = useState(null);

    const [downloading, setDownloading] = useState(null);





    async function loadScans() {

        try {

            const response = await api.get("/scans");

            setScans(response.data);


        } catch (error) {

            console.error(
                "Failed loading scans:",
                error
            );

        } finally {

            setLoading(false);

        }

    }





    useEffect(() => {

        loadScans();

    }, []);








    function formatDate(date) {


        if (!date) {

            return "Unknown";

        }


        return new Date(date).toLocaleString();


    }










    function getStatusClass(status) {


        if (status === "completed") {

            return "status-completed";

        }


        if (status === "failed") {

            return "status-failed";

        }


        return "status-running";


    }










    function getGradeClass(grade) {


        if (!grade) {

            return "";

        }


        return `grade-${grade.toLowerCase()}`;


    }










    function getRiskClass(risk) {


        if (!risk) {

            return "risk-critical";

        }


        return `risk-${risk.toLowerCase()}`;


    }










    function formatDuration(seconds) {


        if (
            seconds === null ||
            seconds === undefined
        ) {

            return "--";

        }


        return `${Number(seconds).toFixed(1)}s`;


    }










    async function deleteScan(id) {


        const confirmDelete = window.confirm(
            "Delete this scan history permanently?"
        );


        if (!confirmDelete) {

            return;

        }





        try {


            setDeleting(id);



            await api.delete(
                `/scans/${id}`
            );



            setScans(
                previousScans =>
                    previousScans.filter(
                        scan => scan.id !== id
                    )
            );


        } catch (error) {


            console.error(
                "Delete failed:",
                error
            );


            alert(
                "Failed to delete scan."
            );


        } finally {


            setDeleting(null);


        }


    }










    async function downloadReport(id) {


        try {


            setDownloading(id);


            await downloadPDFReport(
                id
            );


        } catch (error) {


            console.error(
                "PDF download failed:",
                error
            );


            alert(
                "Unable to download PDF report."
            );


        } finally {


            setDownloading(null);


        }


    }










    if (loading) {


        return (

            <div className="history-empty">

                Loading previous assessments...

            </div>

        );

    }










    if (scans.length === 0) {


        return (

            <section className="history-container">


                <div className="history-empty">

                    No scan history available.

                </div>


            </section>

        );

    }










    return (


        <section className="history-container">



            <div className="section-header">


                <h2>

                    Assessment History

                </h2>



                <p>

                    Previously completed website security assessments.

                </p>


            </div>










            {
                scans.map((scan) => (


                    <article

                        className="history-card"

                        key={scan.id}

                    >



                        <div className="history-main">



                            <h3>

                                {scan.target_url}

                            </h3>





                            <p className="history-date">

                                {formatDate(scan.created_at)}

                            </p>









                            <div className="history-badges">



                                <span

                                    className={
                                        `history-status ${getStatusClass(scan.status)}`
                                    }

                                >

                                    {scan.status}

                                </span>









                                <span

                                    className={
                                        `history-risk ${getRiskClass(scan.risk_level)}`
                                    }

                                >

                                    {scan.risk_level || "Unknown"}

                                </span>



                            </div>


                        </div>













                        <div className="history-metrics">



                            <div>

                                <span>

                                    Score

                                </span>


                                <strong>

                                    {scan.score ?? "--"}

                                </strong>


                            </div>









                            <div>

                                <span>

                                    Grade

                                </span>


                                <strong

                                    className={
                                        getGradeClass(scan.grade)
                                    }

                                >

                                    {scan.grade ?? "--"}

                                </strong>


                            </div>









                            <div>

                                <span>

                                    Findings

                                </span>


                                <strong>

                                    {scan.findings_count ?? "--"}

                                </strong>


                            </div>









                            <div>

                                <span>

                                    Duration

                                </span>


                                <strong>

                                    {formatDuration(scan.duration_seconds)}

                                </strong>


                            </div>









                            <button

                                className="view-report-button"

                                onClick={() => onSelectScan(scan.id)}

                            >

                                View Report

                            </button>









                            {
                                scan.status === "completed" && (

                                    <button

                                        className="download-report-button"

                                        disabled={downloading === scan.id}

                                        onClick={() => downloadReport(scan.id)}

                                    >

                                        {
                                            downloading === scan.id
                                            ? "Downloading..."
                                            : "Download PDF"
                                        }

                                    </button>

                                )
                            }









                            <button

                                className="delete-report-button"

                                disabled={deleting === scan.id}

                                onClick={() => deleteScan(scan.id)}

                            >

                                {
                                    deleting === scan.id
                                    ? "Deleting..."
                                    : "Delete"
                                }

                            </button>




                        </div>


                    </article>


                ))

            }


        </section>


    );


}


export default History;