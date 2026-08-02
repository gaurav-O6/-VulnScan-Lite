import { useMemo, useState } from "react";

import FindingCard from "./FindingCard";

function FindingsList({ findings }) {

    const [filter, setFilter] = useState("all");

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

    const filteredFindings = useMemo(() => {

        let results = findings;

        if (filter === "failed") {

            results = results.filter(
                finding => finding.status === "failed"
            );

        } else if (filter !== "all") {

            results = results.filter(
                finding =>
                    finding.severity?.toLowerCase() === filter
            );

        }

        const severityOrder = {
            high: 0,
            medium: 1,
            low: 2,
            informational: 3
        };

        return [...results].sort((a, b) => {

            if (a.status !== b.status) {

                return a.status === "failed" ? -1 : 1;

            }

            return (
                severityOrder[a.severity?.toLowerCase()] ?? 99
            ) - (
                severityOrder[b.severity?.toLowerCase()] ?? 99
            );

        });

    }, [findings, filter]);

    return (

        <section className="findings-container">

            <div className="section-header">

                <div>

                    <h2>

                        Security Findings

                    </h2>

                    <p>

                        Review detected security issues and recommendations.

                    </p>

                </div>

            </div>

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

            {

                filteredFindings.length === 0 ? (

                    <div className="empty-state">

                        <h3>

                            No Findings

                        </h3>

                        <p>

                            No findings match the selected filter.

                        </p>

                    </div>

                ) : (

                    filteredFindings.map((finding) => (

                        <FindingCard

                            key={finding.id}

                            finding={finding}

                        />

                    ))

                )

            }

        </section>

    );

}

export default FindingsList;