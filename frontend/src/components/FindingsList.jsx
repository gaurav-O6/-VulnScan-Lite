import FindingCard from "./FindingCard";


function FindingsList({ findings }) {


    return (

        <div className="report-card">


            <h2>
                Security Findings
            </h2>



            {

                findings.map(
                    (finding) => (

                        <FindingCard

                            key={finding.id}

                            finding={finding}

                        />

                    )

                )

            }


        </div>

    );

}


export default FindingsList;