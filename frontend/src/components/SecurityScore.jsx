function SecurityScore({ score, grade }) {


    function getRiskLabel(score) {


        if (score >= 90) {

            return "Excellent Security Posture";

        }


        if (score >= 75) {

            return "Good Security Posture";

        }


        if (score >= 50) {

            return "Needs Improvement";

        }


        return "High Risk";

    }





    function getScoreClass(score) {


        if (score >= 90) {

            return "score-good";

        }


        if (score >= 75) {

            return "score-medium";

        }


        return "score-danger";

    }





    return (

        <div className="security-score-card">



            <div
                className={
                    `score-circle ${getScoreClass(score)}`
                }
            >


                <span className="score-number">

                    {score}

                </span>


                <span className="score-outof">

                    /100

                </span>


            </div>





            <div className="score-details">


                <h2>
                    Security Score
                </h2>



                <p>
                    {getRiskLabel(score)}
                </p>




                <div className="grade-badge">

                    Grade {grade}

                </div>



            </div>



        </div>

    );

}


export default SecurityScore;