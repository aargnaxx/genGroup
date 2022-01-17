<template>
  <div class="section">
    <b-field label="Izvještaj">
      <b-select placeholder="Odaberite izvještaj" expanded v-model="selectedId">
        <option v-for="(r, i) in reports" :key="i" :value="i">{{ r.analysis_file }}</option>
      </b-select>
    </b-field>

    <!-- <b-button type="is-primary is-light" @click="getReport"
      >Prikaži izvještaj</b-button
    > -->
    <section v-if="selectedId != -1">
      <br />
      <b-message type="is-info">{{ this.reports[selectedId] }}</b-message>
    </section>
  </div>
</template>


<script lang="ts">
import { Component, Model, Vue } from "vue-property-decorator";
import axios from "axios";

@Component
export default class Reports extends Vue {
  @Model() private reports: any[] = [];
  @Model() private selectedId = -1;
  @Model() private resultString = "";

  private getReports(): void {
    axios({
      method: "get",
      url: "clustering/",
    })
      .then((response) => {
        this.reports = response.data;
        console.log(response);
      })
      .catch(function (response) {
        //handle error
        console.log(response);
      });
  }

  private getReport(): void {
    axios({
      method: "get",
      url: "clustering/" + this.selectedId,
    })
      .then((response) => {
        this.resultString = response.data;
        console.log(response);
      })
      .catch(function (response) {
        //handle error
        console.log(response);
      });
  }

  mounted(): void {
    this.getReports();
  }
}
</script>

<style>
</style>