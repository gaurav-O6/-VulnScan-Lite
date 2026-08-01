function FindingsSummary({ findings }) {


    const total = findings.length;


    const passed = findings.filter(

        item => item.status === "passed"

    ).length;



    const failed = findings.filter(

        item => item.status === "failed"

    ).length;




    const severityCount = {


        High: 0,

        Medium: 0,

        Low: 0,

        Informational: 0

    };





    findings.forEach((finding) => {


        if (severityCount[finding.severity] !== undefined) {

            severityCount[finding.severity]++;

        }


    });





    return (

        <div className="summary-section">


            <h2>
                Assessment Summary
            </h2>




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

                        {
                            failed === 0

                            ? "Low"

                            : failed <= 3

                            ? "Moderate"

                            : "High"

                        }

                    </strong>


                </div>



            </div>




            <div className="severity-breakdown">


                <span>
                    High: {severityCount.High}
                </span>


                <span>
                    Medium: {severityCount.Medium}
                </span>


                <span>
                    Low: {severityCount.Low}
                </span>


                <span>
                    Info: {severityCount.Informational}
                </span>


            </div>



        </div>

    );

}


export default FindingsSummary;
