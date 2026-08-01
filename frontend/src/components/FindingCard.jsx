import { useState } from "react";


function FindingCard({ finding }) {

    const [showEvidence, setShowEvidence] = useState(false);


    const severity =
        finding.severity?.toLowerCase() || "info";


    const status =
        finding.status?.toLowerCase() || "unknown";



    return (

        <div className="finding-card">


            <div className="finding-header">


                <h3>
                    {finding.name}
                </h3>


                <div className="finding-badges">


                    <span
                        className={`severity-badge ${severity}`}
                    >
                        {finding.severity}
                    </span>


                    <span
                        className={`status-badge ${status}`}
                    >
                        {
                            status === "passed"
                                ? "✓ Passed"
                                : "✕ Failed"
                        }
                    </span>


                </div>


            </div>



            <p className="finding-description">

                {finding.description}

            </p>



            {
                finding.evidence &&

                <>

                    <button

                        className="evidence-button"

                        onClick={() =>
                            setShowEvidence(
                                !showEvidence
                            )
                        }

                    >

                        {
                            showEvidence
                                ? "Hide Evidence ▲"
                                : "Show Evidence ▼"
                        }

                    </button>



                    {
                        showEvidence &&

                        <pre className="evidence-box">

                            {finding.evidence}

                        </pre>

                    }

                </>

            }


        </div>

    );

}


export default FindingCard;
