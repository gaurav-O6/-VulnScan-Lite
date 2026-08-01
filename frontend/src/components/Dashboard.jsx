import SecurityScore from "./SecurityScore";
import FindingsSummary from "./FindingsSummary";
import FindingsList from "./FindingsList";


function Dashboard({ scan }) {


    if (!scan?.report) {

        return null;

    }



    return (

        <section className="dashboard">


            <div className="scan-meta-card">


                <div>

                    <span>
                        Target
                    </span>

                    <strong>
                        {scan.target_url}
                    </strong>

                </div>



                <div>

                    <span>
                        Status
                    </span>

                    <strong className="status-complete">
                        Completed
                    </strong>

                </div>



                <div>

                    <span>
                        Score
                    </span>

                    <strong>
                        {scan.score}/100
                    </strong>

                </div>


            </div>





            <SecurityScore

                score={scan.score}

                grade={scan.grade}

            />





            <FindingsSummary

                findings={
                    scan.report.findings || []
                }

            />





            <FindingsList

                findings={
                    scan.report.findings || []
                }

            />


        </section>

    );

}


export default Dashboard;