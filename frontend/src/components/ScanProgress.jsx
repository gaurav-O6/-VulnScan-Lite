function ScanProgress({ scan }) {


    if (!scan) {
        return null;
    }


    return (

        <div className="scan-card">

            <h2>
                Scan Status
            </h2>


            <p>
                Target:
                {" "}
                {scan.target_url}
            </p>


            <p>
                Status:
                {" "}
                <strong>
                    {scan.status}
                </strong>
            </p>


            {
                scan.status === "completed" &&

                <>

                    <p>
                        Score:
                        {" "}
                        {scan.score}/100
                    </p>


                    <p>
                        Grade:
                        {" "}
                        {scan.grade}
                    </p>

                </>

            }


            {
                scan.status === "failed" &&

                <p className="error">
                    Scan failed.
                </p>

            }


        </div>

    );

}


export default ScanProgress;