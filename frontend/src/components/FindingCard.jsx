function FindingCard({ finding }) {


    const severity =
        finding.severity?.toLowerCase() || "informational";


    const status =
        finding.status === "failed"
            ? "failed"
            : "passed";



    return (

        <div className="finding-card">


            <div className="finding-top">


                <h3>
                    {finding.name}
                </h3>



                <span
                    className={`severity-badge ${severity}`}
                >

                    {finding.severity}

                </span>


            </div>





            <div className="finding-status">


                <span>
                    Status
                </span>


                <strong
                    className={status}
                >

                    {
                        finding.status === "failed"
                            ? "✕ Failed"
                            : "✓ Passed"
                    }

                </strong>


            </div>





            <p className="finding-description">

                {finding.description}

            </p>





            {
                finding.evidence &&

                <details className="evidence-box">


                    <summary>

                        View Evidence

                    </summary>



                    <pre>

                        {finding.evidence}

                    </pre>


                </details>

            }




            {
                finding.recommendation &&

                <div className="recommendation">


                    <strong>
                        Recommendation
                    </strong>


                    <p>
                        {finding.recommendation}
                    </p>


                </div>

            }




        </div>

    );

}


export default FindingCard;