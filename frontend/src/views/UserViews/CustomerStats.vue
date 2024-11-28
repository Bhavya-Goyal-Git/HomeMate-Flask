<template>
  <div class="charts-cont">
    <div class="chart-cont">
      <h1>Categories of service Requests booked</h1>
      <canvas id="catpie"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Requests booked daily</h1>
      <canvas id="dateline"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Spending per service Request</h1>
      <canvas id="billbar"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Status of service Requests</h1>
      <canvas id="statuspie"></canvas>
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
const statsData = ref(null);
let categories = {};
let status = {};
let dates = [];
let datedata = {};
let bills = [];
onMounted(async () => {
  backend_req("/customer/stats", "GET", null).then((val) => {
    statsData.value = val;
    lightColors = Array.from({ length: val.length }, generateSoftColor);
    makeCharts();
  });
});
function makeCharts() {
  Array.from(statsData.value).forEach((obj) => {
    dates.push(obj.date);
    bills.push(obj.bill);
    categories[obj.service_cat] = (categories[obj.service_cat] || 0) + 1;
    status[obj.status] = (status[obj.status] || 0) + 1;
    datedata[obj.date] = (datedata[obj.date] || 0) + 1;
  });
  displayCharts();
}
function displayCharts() {
  new Chart(document.getElementById("billbar"), {
    type: "bar",
    data: {
      labels: dates,
      datasets: [
        {
          label: "Money spent on services",
          data: bills,
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
  new Chart(document.getElementById("catpie"), {
    type: "pie", // Chart type
    data: {
      labels: Object.keys(categories), // Customize the labels here
      datasets: [
        {
          label: "Services booked per category",
          backgroundColor: lightColors, // Set the background colors using the generated array
          borderColor: "rgba(0,0,0,0.1)", // Optional border color for each slice
          data: Object.values(categories), // Insert your data here
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
  new Chart(document.getElementById("dateline"), {
    type: "line", // Chart type
    data: {
      labels: Object.keys(datedata), // X-axis labels
      datasets: [
        {
          label: "Services booked on dates", // Name of the dataset
          data: Object.values(datedata), // Y-axis data values
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
            text: "Num Services", // Y-axis title
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

<style>
.charts-cont {
  display: flex;
  flex-wrap: wrap;
  margin-top: 50px;
}
.chart-cont {
  padding: 15px;
  margin: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 700px;
  height: 450px;
}
.chart-cont h1 {
  font-size: 30px;
  margin-bottom: 15px;
}
</style>
