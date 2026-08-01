import { useState } from "react";

import FindingCard from "./FindingCard";


function FindingsList({ findings }) {


    const [filter, setFilter] = useState("all");



    if (!findings || findings.length === 0) {

        return (

            <div className="report-card">

                <h2>
                    Security Findings
                </h2>

                <p>
                    No findings available.
                </p>

            </div>

        );

    }





    const filteredFindings = findings.filter(

        (finding) => {


            if (filter === "all") {

                return true;

            }



            if (filter === "failed") {

                return finding.status === "failed";

            }



            return (

                finding.severity?.toLowerCase() === filter

            );


        }

    );






    const sortedFindings = [

        ...filteredFindings

    ].sort((a, b) => {


        const failedA =
            a.status === "failed" ? 0 : 1;


        const failedB =
            b.status === "failed" ? 0 : 1;



        if (failedA !== failedB) {

            return failedA - failedB;

        }



        return 0;


    });







    const filters = [

        {
            label: "All",
            value: "all"
        },

        {
            label: "Failed",
            value: "failed"
        },

        {
            label: "High",
            value: "high"
        },

        {
            label: "Medium",
            value: "medium"
        },

        {
            label: "Low",
            value: "low"
        }

    ];







    return (

        <div className="findings-container">



            <h2>
                Security Findings
            </h2>





            <div className="filter-bar">


                {
                    filters.map((item) => (

                        <button

                            key={item.value}

                            className={
                                filter === item.value
                                    ? "active-filter"
                                    : ""
                            }

                            onClick={() =>
                                setFilter(item.value)
                            }

                        >

                            {item.label}

                        </button>

                    ))

                }


            </div>







            <div>


                {
                    sortedFindings.map(

                        (finding) => (

                            <FindingCard

                                key={finding.id}

                                finding={finding}

                            />

                        )

                    )

                }



                {
                    sortedFindings.length === 0 &&

                    <div className="report-card">

                        No findings match this filter.

                    </div>

                }



            </div>




        </div>

    );

}


export default FindingsList;
