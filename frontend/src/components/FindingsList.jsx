function FindingsList({ findings }) {


    return (

        <div className="report-card">

            <h2>
                Security Findings
            </h2>



            {
                findings.map(
                    (finding) => (

                        <div
                            key={finding.id}
                            style={{
                                marginTop: "20px",
                                padding: "15px",
                                background: "#334155",
                                borderRadius: "8px"
                            }}
                        >

                            <h3>
                                {finding.name}
                            </h3>


                            <p>
                                Severity:
                                {" "}
                                {finding.severity}
                            </p>


                            <p>
                                Status:
                                {" "}
                                {finding.status}
                            </p>


                            {
                                finding.evidence &&

                                <p>
                                    Evidence:
                                    {" "}
                                    {finding.evidence}
                                </p>

                            }


                        </div>

                    )

                )
            }


        </div>

    );

}


export default FindingsList;