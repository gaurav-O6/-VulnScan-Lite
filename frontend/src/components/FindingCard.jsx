function FindingCard({ finding }) {

    const severity =
        finding.severity?.toLowerCase() || "informational";

    const failed =
        finding.status === "failed";

    function formatEvidence(evidence) {

        if (
            evidence === null ||
            evidence === undefined
        ) {
            return "";
        }

        if (typeof evidence === "string") {
            return evidence;
        }

        return JSON.stringify(
            evidence,
            null,
            2
        );

    }

    return (

        <article className="finding-card">

            <div className="finding-top">

                <div className="finding-title">

                    <div className="finding-meta">

                        {
                            finding.id &&

                            <span className="finding-id">

                                {finding.id}

                            </span>
                        }

                        {
                            finding.category &&

                            <span className="finding-category">

                                {finding.category}

                            </span>
                        }

                    </div>

                    <h3>

                        {finding.title || finding.name}

                    </h3>

                    <p>

                        {finding.description}

                    </p>

                </div>


                <span
                    className={`severity-badge ${severity}`}
                >
                    {finding.severity}
                </span>

            </div>


            <div className="finding-footer">

                <div className="finding-status">

                    <span>

                        Assessment Status

                    </span>

                    <strong
                        className={
                            failed
                                ? "failed"
                                : "passed"
                        }
                    >

                        {failed ? "Failed" : "Passed"}

                    </strong>

                </div>



                <div>

                    {
                        finding.impact &&

                        <div className="recommendation">

                            <strong>

                                Impact

                            </strong>

                            <p>

                                {finding.impact}

                            </p>

                        </div>
                    }


                    {
                        finding.recommendation &&

                        <div className="recommendation">

                            <strong>

                                Remediation

                            </strong>

                            <p>

                                {finding.recommendation}

                            </p>

                        </div>
                    }


                    {
                        finding.reference &&

                        <div className="recommendation">

                            <strong>

                                Reference

                            </strong>

                            <p>

                                {finding.reference}

                            </p>

                        </div>
                    }

                </div>

            </div>



            {
                finding.evidence &&

                <details className="evidence-box">

                    <summary>

                        View Technical Evidence

                    </summary>

                    <pre>

                        {formatEvidence(
                            finding.evidence
                        )}

                    </pre>

                </details>
            }

        </article>

    );

}

export default FindingCard;