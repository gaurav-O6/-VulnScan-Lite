function FindingCard({ finding }) {

    const severity =
        finding.severity?.toLowerCase() || "informational";

    const failed =
        finding.status === "failed";

    return (

        <article className="finding-card">

            <div className="finding-top">

                <div className="finding-title">

                    <h3>
                        {finding.name}
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


            </div>



            {
                finding.evidence &&

                <details className="evidence-box">

                    <summary>
                        View Technical Evidence
                    </summary>


                    <pre>
                        {finding.evidence}
                    </pre>


                </details>
            }


        </article>

    );

}


export default FindingCard;
