import { useEffect, useState } from "react";
import api from "../api/client";
import "../styles/history.css";


function History({ onSelectScan }) {


    const [scans, setScans] = useState([]);

    const [loading, setLoading] = useState(true);



    useEffect(() => {


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





    function getFindingCount(scan) {


        if (scan.findings_count !== undefined) {

            return scan.findings_count;

        }


        if (scan.total_findings !== undefined) {

            return scan.total_findings;

        }


        if (Array.isArray(scan.findings)) {

            return scan.findings.length;

        }


        return "--";


    }





    function getRiskLabel(score) {


        if (score === null || score === undefined) {

            return "Unknown Risk";

        }


        if (score >= 90) {

            return "Low Risk";

        }


        if (score >= 70) {

            return "Medium Risk";

        }


        if (score >= 40) {

            return "High Risk";

        }


        return "Critical Risk";


    }





    function getRiskClass(score) {


        if (score === null || score === undefined) {

            return "risk-critical";

        }


        if (score >= 90) {

            return "risk-low";

        }


        if (score >= 70) {

            return "risk-medium";

        }


        if (score >= 40) {

            return "risk-high";

        }


        return "risk-critical";


    }





    if (loading) {


        return (

            <div className="history-empty">

                Loading previous assessments...

            </div>

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
                                        `history-risk ${getRiskClass(scan.score)}`
                                    }

                                >

                                    {getRiskLabel(scan.score)}

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

                                    {getFindingCount(scan)}

                                </strong>


                            </div>





                            <button

                                className="view-report-button"

                                onClick={() => onSelectScan(scan.id)}

                            >

                                View Report

                            </button>



                        </div>


                    </article>


                ))

            }


        </section>

    );


}


export default History;