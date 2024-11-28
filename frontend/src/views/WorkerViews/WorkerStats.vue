<template>
  <div class="charts-cont">
    <div class="chart-cont">
      <h1>Status of service Requests</h1>
      <canvas id="statuspie"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Requests recieved per day</h1>
      <canvas id="reqrecieveline"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Earning per service Request</h1>
      <canvas id="earningbar"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Star Ratings recieved perecentages</h1>
      <canvas id="starspie"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Average rating recieved daily</h1>
      <canvas id="avgratingline"></canvas>
    </div>
  </div>
</template>

<script setup>
import { backend_req } from "@/composables/requestbackend";
import { onMounted, ref } from "vue";
import {
  Chart,
  LinearScale,
  CategoryScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  BarController,
  PieController,
  ArcElement,
  LineController,
  PointElement,
  LineElement,
  Filler,
} from "chart.js";

Chart.register(
  LinearScale,
  CategoryScale,
  BarElement,
  BarController,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PieController,
  LineController,
  PointElement,
  LineElement,
  Filler
);
function generateSoftColor() {
  const h = Math.floor(Math.random() * 360);
  const s = Math.floor(Math.random() * 20) + 40;
  const l = Math.floor(Math.random() * 20) + 60;
  return `hsl(${h}, ${s}%, ${l}%)`;
}
let lightColors = null;
const servstatsData = ref(null);
const revistatsData = ref(null);
let maxlen = 0;
onMounted(async () => {
  backend_req("/professional/servicestats", "GET", null)
    .then((val) => {
      servstatsData.value = val;
      maxlen = val.length;
    })
    .then((val) => {
      return backend_req("/professional/reviewstats", "GET", null);
    })
    .then((val) => {
      revistatsData.value = val;
      if (val.length > maxlen) maxlen = val.length;
      lightColors = Array.from({ length: maxlen }, generateSoftColor);
      makeCharts();
    });
});

let status = {};
let reqrecieve = {};
let earning = [];
let dates = [];
let stars = {};
let datestars = {}; //useless
let datestarnum = {}; //useless
let dateAvgRate = {};
function makeCharts() {
  Array.from(servstatsData.value).forEach((obj) => {
    status[obj.status] = (status[obj.status] || 0) + 1;
    reqrecieve[obj.daterecieve] = (reqrecieve[obj.daterecieve] || 0) + 1;
    dates.push(obj.date);
    earning.push(obj.earning);
  });
  Array.from(revistatsData.value).forEach((obj) => {
    stars[obj.stars] = (stars[obj.stars] || 0) + 1;
    datestars[obj.date] = (datestars[obj.date] || 0) + obj.stars;
    datestarnum[obj.date] = (datestarnum[obj.date] || 0) + 1;
  });
  for (const key in datestars) {
    dateAvgRate[key] = datestars[key] / datestarnum[key];
  }
  displayCharts();
}
function displayCharts() {
  new Chart(document.getElementById("statuspie"), {
    type: "pie", // Chart type
    data: {
      labels: Object.keys(status), // Customize the labels here
      datasets: [
        {
          label: "Statuses of Service Requests",
          data: Object.values(status),
          backgroundColor: lightColors, // Set the background colors using the generated array
          borderColor: "rgba(0,0,0,0.1)", // Optional border color for each slice
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top", // Legend position: 'top', 'bottom', 'left', 'right'
        },
      },
    },
  });
  new Chart(document.getElementById("reqrecieveline"), {
    type: "line", // Chart type
    data: {
      labels: Object.keys(reqrecieve), // X-axis labels
      datasets: [
        {
          label: "Requests recieved on dates", // Name of the dataset
          data: Object.values(reqrecieve), // Y-axis data values
          backgroundColor: "rgba(75, 192, 192, 0.2)", // Fill color below the line
          borderColor: "rgba(75, 192, 192, 1)", // Line color
          borderWidth: 2, // Line width
          fill: true, // Whether to fill the area under the line
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: "Dates", // X-axis title
          },
        },
        y: {
          title: {
            display: true,
            text: "Num Requests", // Y-axis title
          },
          beginAtZero: true, // Ensure Y-axis starts at 0
        },
      },
      plugins: {
        legend: {
          position: "top", // Legend position: 'top', 'bottom', 'left', 'right'
        },
      },
    },
  });
  new Chart(document.getElementById("earningbar"), {
    type: "bar",
    data: {
      labels: dates,
      datasets: [
        {
          label: "Money earned on requests",
          data: earning,
          backgroundColor: lightColors, // Set the background colors using the generated array
          borderColor: "rgba(0,0,0,0.1)", // Optional border color for each slice
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return "₹" + value; // Prefix each tick with a dollar sign
            },
          },
        },
      },
    },
  });
  new Chart(document.getElementById("starspie"), {
    type: "pie", // Chart type
    data: {
      labels: Object.keys(stars), // Customize the labels here
      datasets: [
        {
          label: "Star Ratings recieved",
          data: Object.values(stars),
          backgroundColor: lightColors, // Set the background colors using the generated array
          borderColor: "rgba(0,0,0,0.1)", // Optional border color for each slice
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top", // Legend position: 'top', 'bottom', 'left', 'right'
        },
      },
    },
  });
  new Chart(document.getElementById("avgratingline"), {
    type: "line", // Chart type
    data: {
      labels: Object.keys(dateAvgRate), // X-axis labels
      datasets: [
        {
          label: "Average rating daily", // Name of the dataset
          data: Object.values(dateAvgRate), // Y-axis data values
          backgroundColor: "rgba(75, 192, 192, 0.2)", // Fill color below the line
          borderColor: "rgba(75, 192, 192, 1)", // Line color
          borderWidth: 2, // Line width
          fill: true, // Whether to fill the area under the line
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: "Dates", // X-axis title
          },
        },
        y: {
          title: {
            display: true,
            text: "Average Rating", // Y-axis title
          },
          beginAtZero: true, // Ensure Y-axis starts at 0
        },
      },
      plugins: {
        legend: {
          position: "top", // Legend position: 'top', 'bottom', 'left', 'right'
        },
      },
    },
  });
}
</script>

<style></style>
