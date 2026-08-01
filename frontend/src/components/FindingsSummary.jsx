function FindingsSummary({ findings }) {


    const failed = findings.filter(
        item => item.status === "failed"
    );


    const passed = findings.filter(
        item => item.status === "passed"
    );


    const severity = {
        High: 0,
        Medium: 0,
        Low: 0,
    };


    failed.forEach(item => {

        if (severity[item.severity] !== undefined) {

            severity[item.severity]++;

        }

    });



    return (

        <div className="report-card">

            <h2>
                Findings Summary
            </h2>


            <p>
                Total Findings: {findings.length}
            </p>


            <p>
                Passed: {passed.length}
            </p>


            <p>
                Failed: {failed.length}
            </p>


            <br />


            <p>
                High: {severity.High}
            </p>


            <p>
                Medium: {severity.Medium}
            </p>


            <p>
                Low: {severity.Low}
            </p>


        </div>

    );

}


export default FindingsSummary;