// scripts.js
document.addEventListener('DOMContentLoaded', function() {
    fetch('/get-data/')
        .then(response => response.json())
        .then(data => {
            renderPatientOverview(data.patient_data);
            renderBedManagement(data.bed_data);
            // Render other charts similarly
        })
        .catch(error => console.error('Error fetching data:', error));
});

function renderPatientOverview(data) {
    // Render patient overview charts using Plotly.js
}

function renderBedManagement(data) {
    // Render bed management chart using Plotly.js
    // Example:
    const dates = data.map(item => item.date);
    const totalBeds = data.map(item => item.total_beds);
    const occupiedBeds = data.map(item => item.occupied_beds);

    const bedManagementChart = {
        x: dates,
        y: [totalBeds, occupiedBeds],
        type: 'scatter',
        mode: 'lines',
        name: 'Total Beds'
    };

    const bedManagementLayout = {
        title: 'Bed Management',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Number of Beds' }
    };

    Plotly.newPlot('bedManagement', [bedManagementChart], bedManagementLayout);
}
