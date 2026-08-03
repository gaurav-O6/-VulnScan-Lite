import {
    RadialBarChart,
    RadialBar,
    ResponsiveContainer,
} from "recharts";



function SecurityScore({ score, grade }) {


    const currentScore = score ?? 0;



    function getRiskLabel(value) {


        if (value >= 90) {

            return "Excellent Security Posture";

        }


        if (value >= 75) {

            return "Good Security Posture";

        }


        if (value >= 50) {

            return "Moderate Risk";

        }


        return "High Risk";


    }






    function getGaugeColor(value) {


        if (value >= 90) {

            return "#4ade80";

        }


        if (value >= 75) {

            return "#38bdf8";

        }


        if (value >= 50) {

            return "#facc15";

        }


        return "#f87171";


    }






    function getScoreClass(value) {


        if (value >= 90) {

            return "score-excellent";

        }


        if (value >= 75) {

            return "score-good";

        }


        if (value >= 50) {

            return "score-medium";

        }


        return "score-danger";


    }






    const gaugeData = [

        {
            name: "Security Score",
            value: currentScore,
            fill: getGaugeColor(currentScore),
        },

    ];






    return (

        <section className="security-score-card">





            <div
                className={`score-gauge ${getScoreClass(currentScore)}`}
            >


                <ResponsiveContainer
                    width="100%"
                    height="100%"
                >


                    <RadialBarChart

                        cx="50%"

                        cy="50%"

                        innerRadius="70%"

                        outerRadius="100%"

                        startAngle={90}

                        endAngle={-270}

                        data={gaugeData}

                    >


                        <RadialBar

                            dataKey="value"

                            cornerRadius={20}

                            background

                            animationDuration={1200}

                        />


                    </RadialBarChart>


                </ResponsiveContainer>






                <div className="gauge-center">


                    <span className="score-number">

                        {currentScore}

                    </span>


                    <span className="score-outof">

                        /100

                    </span>


                </div>


            </div>








            <div className="score-details">



                <span className="score-title">

                    Security Rating

                </span>





                <h2>

                    {getRiskLabel(currentScore)}

                </h2>





                <p>

                    Overall security posture based on detected
                    vulnerabilities and configuration checks.

                </p>







                <div className="score-stats">



                    <div className="score-stat-box">


                        <span>

                            Grade

                        </span>


                        <strong>

                            {grade || "N/A"}

                        </strong>


                    </div>







                    <div className="score-stat-box">


                        <span>

                            Assessment

                        </span>


                        <strong className="assessment-status">

                            Completed

                        </strong>


                    </div>



                </div>




            </div>




        </section>


    );


}


export default SecurityScore;