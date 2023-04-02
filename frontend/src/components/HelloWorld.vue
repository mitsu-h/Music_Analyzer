<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <button @click="fetchData">Fetch Data from Django</button>
    <p>{{ apiData.message }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
  data() {
    return {
      apiData: {},
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get("http://localhost:8081/api/hello/");
        this.apiData = response.data;
    } catch (error) {
      console.error('API request error:', error);
    }
  },
}
}
</script>