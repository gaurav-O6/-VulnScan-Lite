function FindingsSummary({ findings }) {

    const total = findings.length;

    const passed = findings.filter(
        finding => finding.status === "passed"
    ).length;

    const failed = findings.filter(
        finding => finding.status === "failed"
    ).length;


    const severity = {

        High: 0,
        Medium: 0,
        Low: 0,
        Informational: 0

    };


    findings.forEach((finding) => {

        if (severity[finding.severity] !== undefined) {

            severity[finding.severity]++;

        }

    });


    const risk =
        failed === 0
            ? "Low"
            : failed <= 3
                ? "Moderate"
                : "High";


    return (

        <section className="summary-section">


            <div className="section-header">

                <div>

                    <h2>
                        Assessment Summary
                    </h2>

                    <p>
                        Overall results from the passive security assessment.
                    </p>

                </div>

            </div>



            <div className="summary-grid">


                <div className="summary-card">

                    <span>
                        Total Findings
                    </span>

                    <strong>
                        {total}
                    </strong>

                </div>



                <div className="summary-card success">

                    <span>
                        Passed
                    </span>

                    <strong>
                        {passed}
                    </strong>

                </div>



                <div className="summary-card danger">

                    <span>
                        Failed
                    </span>

                    <strong>
                        {failed}
                    </strong>

                </div>



                <div className="summary-card">

                    <span>
                        Risk Level
                    </span>

                    <strong>
                        {risk}
                    </strong>

                </div>


            </div>



            <div className="severity-breakdown">


                <div className="severity-pill high">

                    <span>
                        High
                    </span>

                    <strong>
                        {severity.High}
                    </strong>

                </div>



                <div className="severity-pill medium">

                    <span>
                        Medium
                    </span>

                    <strong>
                        {severity.Medium}
                    </strong>

                </div>



                <div className="severity-pill low">

                    <span>
                        Low
                    </span>

                    <strong>
                        {severity.Low}
                    </strong>

                </div>



                <div className="severity-pill informational">

                    <span>
                        Info
                    </span>

                    <strong>
                        {severity.Informational}
                    </strong>

                </div>


            </div>


        </section>

    );

}


export default FindingsSummary;
