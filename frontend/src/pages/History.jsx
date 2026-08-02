import { useEffect, useState } from "react";
import api from "../api/client";

function History({ onSelectScan }) {

    const [scans, setScans] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        async function loadScans() {

            try {

                const response = await api.get("/scans");

                setScans(response.data);

            } catch (error) {

                console.error("Failed loading scans:", error);

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

                <div>

                    <h2>

                        Assessment History

                    </h2>

                    <p>

                        Previously completed website security assessments.

                    </p>

                </div>

            </div>

            {

                scans.length === 0 &&

                <div className="history-empty">

                    No previous scans available.

                </div>

            }

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

                            <span
                                className={`history-status ${getStatusClass(scan.status)}`}
                            >

                                {scan.status}

                            </span>

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