<template>
  <div class="hero-section">
    <h1 class="hero-heading">Your Home, Our Priority</h1>
    <p class="hero-para">
      Register and book out of 50+ professional services, at your ease, at low
      costs.
    </p>
    <button class="animated-button" @click="$router.push({ name: 'signup' })">
      <svg viewBox="0 0 24 24" class="arr-2" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M16.1716 10.9999L10.8076 5.63589L12.2218 4.22168L20 11.9999L12.2218 19.778L10.8076 18.3638L16.1716 12.9999H4V10.9999H16.1716Z"
        ></path>
      </svg>
      <span class="text">Book A Service Today!</span>
      <span class="circle"></span>
      <svg viewBox="0 0 24 24" class="arr-1" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M16.1716 10.9999L10.8076 5.63589L12.2218 4.22168L20 11.9999L12.2218 19.778L10.8076 18.3638L16.1716 12.9999H4V10.9999H16.1716Z"
        ></path>
      </svg>
    </button>
  </div>
  <div class="main-section">
    <h1 class="hero-heading second-heading">Are you a Service Professional?</h1>
    <p class="hero-para second-para">
      Join 700+ other professionals, discover 1000+ registered, local customers
      for your service.
    </p>
    <button
      class="animated-button second-button"
      @click="$router.push({ name: 'signup' })"
    >
      <svg viewBox="0 0 24 24" class="arr-2" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M16.1716 10.9999L10.8076 5.63589L12.2218 4.22168L20 11.9999L12.2218 19.778L10.8076 18.3638L16.1716 12.9999H4V10.9999H16.1716Z"
        ></path>
      </svg>
      <span class="text">Register and Discover Customers!</span>
      <span class="circle"></span>
      <svg viewBox="0 0 24 24" class="arr-1" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M16.1716 10.9999L10.8076 5.63589L12.2218 4.22168L20 11.9999L12.2218 19.778L10.8076 18.3638L16.1716 12.9999H4V10.9999H16.1716Z"
        ></path>
      </svg>
    </button>
  </div>
</template>

<script setup></script>

<style>
.hero-section {
  background-image: url("/homepic.jpg");
  background-position: center;
}
.hero-section,
.main-section {
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  height: 650px;
}
.main-section {
  background-image: url("/professionals.jpg");
  background-position: top;
}

.hero-heading {
  font-size: 120px;
  color: white;
  font-weight: bolder;
  -webkit-text-stroke: 4px black;
  text-shadow: 30px 30px 60px rgba(0, 0, 0, 0.8);
  margin-bottom: 10px;
  text-align: center;
  line-height: 100px;
}
.hero-heading.second-heading {
  margin-bottom: 10px;
  margin-top: 220px;
}
.hero-para {
  color: white;
  margin-bottom: 60px;
  font-size: 30px;
  -webkit-text-stroke: 0.5px black;
  text-shadow: 10px 10px 30px rgba(0, 0, 0, 0.8);
}
.hero-para.second-para {
  margin-bottom: 30px;
}

.animated-button {
  position: relative;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 16px 36px;
  border: 6px solid;
  border-color: transparent;
  font-size: 32px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 100px;
  font-weight: 600;
  color: greenyellow;
  box-shadow: 0 0 0 3px greenyellow;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
}

.animated-button svg {
  position: absolute;
  width: 30px;
  fill: greenyellow;
  z-index: 9;
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.animated-button .arr-1 {
  right: 16px;
}

.animated-button .arr-2 {
  left: -25%;
}

.animated-button .circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  background-color: greenyellow;
  border-radius: 50%;
  opacity: 0;
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}
.animated-button.second-button .circle {
  width: 70px;
  height: 70px;
}

.animated-button .text {
  position: relative;
  z-index: 1;
  transform: translateX(-24px);
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
  text-shadow: 5px 5px 5px rgba(0, 0, 0, 0.8);
}

.animated-button:hover {
  box-shadow: 0 0 0 12px transparent;
  color: #212121;
  border-radius: 12px;
  background-color: inherit;
}

.animated-button:hover .arr-1 {
  right: -25%;
}

.animated-button:hover .arr-2 {
  left: 16px;
}

.animated-button:hover .text {
  transform: translateX(12px);
  text-shadow: 0 0 0 black;
}

.animated-button:hover svg {
  fill: #212121;
}

.animated-button:active {
  scale: 0.95;
  box-shadow: 0 0 0 4px greenyellow;
}

.animated-button:hover .circle {
  width: 440px;
  height: 440px;
  opacity: 1;
}
.animated-button.second-button:hover .circle {
  width: 660px;
  height: 660px;
  opacity: 1;
}
</style>
