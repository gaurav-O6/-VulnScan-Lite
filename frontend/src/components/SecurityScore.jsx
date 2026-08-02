       function SecurityScore({ score, grade }) {


    function getRiskLabel(score) {

        if (score >= 90) {

            return "Excellent Security Posture";

        }


        if (score >= 75) {

            return "Good Security Posture";

        }


        if (score >= 50) {

            return "Moderate Risk";

        }


        return "High Risk";

    }




    function getScoreClass(score) {

        if (score >= 75) {

            return "score-good";

        }


        if (score >= 50) {

            return "score-medium";

        }


        return "score-danger";

    }




    return (

        <section className="security-score-card">


            <div
                className={`score-circle ${getScoreClass(score)}`}
            >

                <span className="score-number">

                    {score ?? 0}

                </span>


                <span className="score-outof">

                    /100

                </span>


            </div>





            <div className="score-details">


                <span className="score-title">

                    Security Rating

                </span>


                <h2>

                    {getRiskLabel(score)}

                </h2>


                <p>

                    Overall security posture based on detected
                    vulnerabilities and configuration checks.

                </p>





                <div className="score-stats">


                    <div>

                        <span>

                            Grade

                        </span>


                        <strong>

                            {grade || "N/A"}

                        </strong>


                    </div>





                    <div>

                        <span>

                            Assessment

                        </span>


                        <strong>

                            Completed

                        </strong>


                    </div>


                </div>


            </div>


        </section>

    );

}


export default SecurityScore;