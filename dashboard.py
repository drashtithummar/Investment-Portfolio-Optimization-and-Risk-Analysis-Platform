// This script creates an interactive JavaScript dashboard for portfolio visualization
const data = fetch('https://secure-bucket.s3.amazonaws.com/optimized_weights.json')
  .then(response => response.json());

const renderChart = (data) => {
    const ctx = document.getElementById('portfolioChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Optimized Weights',
                data: Object.values(data),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
};

renderChart(data);
