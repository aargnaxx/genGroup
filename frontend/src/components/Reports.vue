<template>
  <div class="section">
    <div class="section">
      <b-button
        label="Dohvati statuse analize"
        type="is-primary"
        size="is-medium"
        @click="getStatuses"
      />
    </div>
    <b-field label="Izvještaj">
      <b-select placeholder="Odaberite izvještaj" expanded v-model="selectedId">
        <option v-for="(r, i) in reports" :key="i" :value="i">
          {{ r.analysis_file }}
        </option>
      </b-select>
    </b-field>

    <!-- <b-button type="is-primary is-light" @click="getReport"
      >Prikaži izvještaj</b-button
    > -->
    <section v-if="selectedId != -1">
      <br />
      <b-message type="is-info">{{ this.reports[selectedId] }}</b-message>
    </section>

    <b-modal v-model="isReportsModalActive">
      <div class="box">
        <b-table
          :data="statuses"
          :columns="columns"
          :bordered="true"
          checkable
          :checkbox-position="left"
          :checked-rows.sync="checkedRows"
        >
          <template #bottom-left>
            <b-button
              size="is-medium"
              icon-left="download"
              @click="download"
            >
              Download
            </b-button>
          </template>
        </b-table>
      </div>
    </b-modal>
  </div>
</template>


<script lang="ts">
import { Component, Model, Vue } from "vue-property-decorator";
import axios from "axios";

@Component
export default class Reports extends Vue {
  @Model() private reports: any[] = [];
  @Model() private checkedRows: any[] = [];
  @Model() private statuses: any[] = [];
  @Model() private selectedId = -1;
  @Model() private isReportsModalActive = false;
  @Model() private resultString = "";
  @Model() private columns: any = [
    {
      field: "id",
      label: "ID",
      width: "40",
      numeric: true,
    },
    {
      field: "analysis_file",
      label: "Datoteka",
    },
    {
      field: "num_clusters",
      label: "Broj klustera",
    },
    {
      field: "sequence_length",
      label: "Dužina sekvence",
    },
    {
      field: "clustering_type",
      label: "Vrsta clusteriranja",
    },
    {
      field: "status",
      label: "Status",
    },
  ];

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

  private getStatuses(): void {
    const loadingComponent = this.$buefy.loading.open({
      container: null,
    });

    axios({
      method: "get",
      url: "clustering/status",
    })
      .then((response) => {
        this.statuses = response.data;
        this.statuses.forEach((element) => {
          switch (element.status) {
            case "UN":
              element.status = "Nepoznat status";
              break;
            case "FA":
              element.status = "Analiza neuspješna";
              break;
            case "SU":
              element.status = "Analiza uspješna";
              break;
            case "IP":
              element.status = "Analiza se trenutno obavlja";
              break;
          }
          element.download =
            '<button @click="console.log(props.id)">Download</button>';
        });
        this.isReportsModalActive = true;
        console.log(response);
      })
      .catch(function (response) {
        //handle error
        console.log(response);
      })
      .finally(() => {
        loadingComponent.close();
      });
  }

  mounted(): void {
    this.getReports();
  }

  download() {
    this.checkedRows.forEach(element => {
      this.downloadItem({url:'clustering/download/'+element.id,label:element.id+'.fasta'})
    });
  }

  downloadItem ({ url, label }) {
    axios.get(url, { responseType: 'blob' })
      .then(response => {
        const blob = new Blob([response.data], { type: 'text/plain' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = label
        link.click()
        URL.revokeObjectURL(link.href)
      }).catch(console.error)
  }
}
</script>

<style>
</style>