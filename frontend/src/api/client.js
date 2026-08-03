import axios from "axios";


const api = axios.create({

    baseURL: "http://127.0.0.1:5000/api",

    headers: {
        "Content-Type": "application/json",
    },

});



export async function downloadPDFReport(scanId) {

    const response = await api.get(
        `/scans/${scanId}/report/pdf`,
        {
            responseType: "blob",
        }
    );


    const blob = new Blob(
        [response.data],
        {
            type: "application/pdf",
        }
    );


    const url = window.URL.createObjectURL(
        blob
    );


    const link = document.createElement(
        "a"
    );


    link.href = url;


    link.download = `vulnscan-report-${scanId}.pdf`;


    document.body.appendChild(
        link
    );


    link.click();


    link.remove();


    window.URL.revokeObjectURL(
        url
    );

}


export default api;