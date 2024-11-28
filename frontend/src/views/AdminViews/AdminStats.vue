<template>
  <div class="charts-cont">
    <div class="chart-cont">
      <h1>User Type Distribution</h1>
      <canvas id="userpie"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Average price per Service Category</h1>
      <canvas id="avgpricebar"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Professionals per Service Category</h1>
      <canvas id="numprofsline"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Services per Service Category</h1>
      <canvas id="catcounts"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Statuses of Service Requests</h1>
      <canvas id="statuspie"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Earning per day</h1>
      <canvas id="earningline"></canvas>
    </div>
    <div class="chart-cont">
      <h1>Star reviews recieved</h1>
      <canvas id="starspie"></canvas>
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
let maxlen = 0;
onMounted(() => {
  backend_req("/stats", "GET", null).then((val) => {
    statsData.value = val;
    maxlen = Object.keys(statsData.value.earning_perDay).length;
    if (maxlen < statsData.value.service_cat_count.length)
      maxlen = statsData.value.service_cat_count.length;
    console.log(maxlen);
    lightColors = Array.from({ length: maxlen }, generateSoftColor);
    makeGraphs();
  });
});
function makeGraphs() {
  new Chart(document.getElementById("userpie"), {
    type: "pie", // Chart type
    data: {
      labels: statsData.value.userdata.map((s) => s.role), // Customize the labels here
      datasets: [
        {
          label: "Users per role",
          backgroundColor: lightColors, // Set the background colors using the generated array
          borderColor: "rgba(0,0,0,0.1)", // Optional border color for each slice
          data: statsData.value.userdata.map((s) => s.count), // Insert your data here
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
  new Chart(document.getElementById("avgpricebar"), {
    type: "bar",
    data: {
      labels: statsData.value.service_cat_avgprice.map((s) => s.cat),
      datasets: [
        {
          label: "Average price per Service Category",
          data: statsData.value.service_cat_avgprice.map((s) => s.avgprice),
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
  new Chart(document.getElementById("numprofsline"), {
    type: "line", // Chart type
    data: {
      labels: statsData.value.service_cat_numprofs.map((s) => s.cat), // X-axis labels
      datasets: [
        {
          label: "Professionals of this service category", // Name of the dataset
          data: statsData.value.service_cat_numprofs.map((s) => s.count), // Y-axis data values
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
  new Chart(document.getElementById("catcounts"), {
    type: "pie", // Chart type
    data: {
      labels: statsData.value.service_cat_count.map((s) => s.cat), // Customize the labels here
      datasets: [
        {
          label: "Number of Services per Service Category",
          data: statsData.value.service_cat_count.map((s) => s.count),
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
  new Chart(document.getElementById("statuspie"), {
    type: "pie", // Chart type
    data: {
      labels: statsData.value.servReq_status.map((s) => s.status), // Customize the labels here
      datasets: [
        {
          label: "Service Requests in status",
          backgroundColor: lightColors, // Set the background colors using the generated array
          borderColor: "rgba(0,0,0,0.1)", // Optional border color for each slice
          data: statsData.value.servReq_status.map((s) => s.count), // Insert your data here
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
  new Chart(document.getElementById("starspie"), {
    type: "pie", // Chart type
    data: {
      labels: statsData.value.stars_dist.map((s) => s.star), // Customize the labels here
      datasets: [
        {
          label: "Service Requests in status",
          backgroundColor: lightColors, // Set the background colors using the generated array
          borderColor: "rgba(0,0,0,0.1)", // Optional border color for each slice
          data: statsData.value.stars_dist.map((s) => s.count), // Insert your data here
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
  new Chart(document.getElementById("earningline"), {
    type: "line", // Chart type
    data: {
      labels: Object.keys(statsData.value.earning_perDay), // X-axis labels
      datasets: [
        {
          label: "Earning per day", // Name of the dataset
          data: Object.values(statsData.value.earning_perDay), // Y-axis data values
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

<style></style>
