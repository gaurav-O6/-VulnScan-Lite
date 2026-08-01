function SecurityScore({ score, grade }) {

    return (

        <div className="report-card">

            <h2>
                Security Score
            </h2>


            <h1>
                {score}/100
            </h1>


            <p>
                Grade: {grade}
            </p>


        </div>

    );

}


export default SecurityScore;