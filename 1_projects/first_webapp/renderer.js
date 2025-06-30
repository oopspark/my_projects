const Database = require('better-sqlite3');
const path = require('path');

const dbPath = path.join(__dirname, 'data.db');
const db = new Database(dbPath);

function getSalesData() {
  const rows = db.prepare('SELECT date, amount FROM sales ORDER BY date').all();
  return rows;
}

window.onload = () => {
  const data = getSalesData();

  const labels = data.map(r => r.date);
  const amounts = data.map(r => r.amount);

  const ctx = document.getElementById('chart').getContext('2d');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: '매출액',
        data: amounts,
        borderColor: 'white',
        backgroundColor: 'rgba(255, 255, 255, 0.2)',
        fill: true,
        tension: 0.2,
        pointBackgroundColor: 'white',
        pointBorderColor: 'white',
        pointHoverBackgroundColor: 'white',
        pointHoverBorderColor: 'white'
      }]
    },
    options: {
      responsive: true,  // 여기를 true로 변경
      plugins: {
        legend: {
          labels: {
            color: 'white'
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: 'white'
          },
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: 'white'
          },
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        }
      }
    }
  });
};
