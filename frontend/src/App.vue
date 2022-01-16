<template>
  <div id="app">
    <section class="hero is-info">
      <div class="hero-body">
        <p class="title">GenGroup</p>
      </div>
    </section>
    <div class="box">
      <b-tabs type="is-toggle" expanded destroy-on-hide="true">
        <b-tab-item label="Upload" icon="upload">
              <Upload/>
        </b-tab-item>
        <b-tab-item label="Preprocess" icon="upload">
              <Preprocessing/>
        </b-tab-item>
        <b-tab-item label="Pokreni analize" icon="chart-box">
          <StartClustering/>
        </b-tab-item>
        <b-tab-item label="Izvještaji" icon="note-text">
          <Reports/>
        </b-tab-item>
        
      </b-tabs>
    </div>
  </div>
</template>


<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Upload from '@/components/Upload.vue'; // @ is an alias to /src
import StartClustering from '@/components/StartClustering.vue'; // @ is an alias to /src
import Reports from '@/components/Reports.vue'; // @ is an alias to /src
import Preprocessing from '@/components/Preprocessing.vue'; // @ is an alias to /src

@Component({
  components: {
    Upload,
    StartClustering,
    Reports,
    Preprocessing
  },
})
export default class MainApp extends Vue {
}
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
