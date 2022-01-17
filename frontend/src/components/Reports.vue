<template>
  <div class="section">
    <b-field label="Vrsta izvještaja">
      <b-select placeholder="Odaberite izvještaj" expanded v-model="reportType">
        <option value="0">Prva vrsta izvještaja</option>
        <option value="1">Druga vrsta izvještaja</option>
        <option value="2">Usporedba s drugom datotekom</option>
      </b-select>
    </b-field>

    <b-button type="is-primary is-light" @click="getReport"
      >Prikaži izvještaj</b-button
    >
    <section v-if="resultString != ''">
      <br />
      <b-message type="is-info">{{ this.resultString }}</b-message>
    </section>
  </div>
</template>


<script lang="ts">
import { Component, Model, Vue } from "vue-property-decorator";
import axios from "axios";

@Component
export default class Reports extends Vue {
  @Model() private reports: any[] = [];
  @Model() private selectedId = 1;
  @Model() private resultString = "";

  private getReports(): void {
    axios({
      method: "get",
      url: "http://localhost:8001/clustering/",
    })
      .then((response) => {
        this.reports = response.data.files;
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
      url: "http://localhost:8001/clustering/" + this.selectedId,
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