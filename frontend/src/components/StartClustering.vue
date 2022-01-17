<template>
  <div>
    <b-field>
      <b-radio-button
        v-model="radioButton"
        native-value="spectral"
        type="is-primary is-light is-outlined"
      >
        <span>Spectral clustering</span>
      </b-radio-button>

      <b-radio-button
        v-model="radioButton"
        native-value="kmedoids"
        type="is-success is-light is-outlined"
      >
        <span>Kmedoids clustering</span>
      </b-radio-button>

      <b-radio-button
        v-model="radioButton"
        native-value="agglomerative"
        type="is-info is-light is-outlined"
      >
        <span>Agglomerative clustering</span>
      </b-radio-button>
    </b-field>
    <b-field grouped>
      <b-field label="Broj klustera" expanded>
        <b-numberinput v-model="clusterNumber"></b-numberinput>
      </b-field>
      <b-field label="Dužina čitanja" expanded>
        <b-numberinput v-model="reading_length"></b-numberinput>
      </b-field>
    </b-field>
    <b-field label="Datoteka">
      <b-select placeholder="Odaberi datoteku" expanded v-model="file">
        <option v-for="(option, i) in files" :value="option" :key="i">
          {{ option }}
        </option>
      </b-select>
    </b-field>
    <b-button type="is-primary" @click="startClustering">Započni</b-button>
  </div>
</template>

<script lang="ts">
import { Component, Model, Vue } from "vue-property-decorator";
import axios from "axios";

@Component
export default class StartClustering extends Vue {
  @Model() private dropFiles: string[] = [];
  @Model() private radioButton = "kmedoids";
  @Model() private file = "";
  @Model() private clusterNumber = 0;
  @Model() private reading_length = 0;

  private files: string[] = [];

  mounted(): void {
    axios({
      method: "get",
      url: "files/",
    })
      .then((response) => {
        this.files = response.data.files;
        console.log(response);
      })
      .catch(function (response) {
        //handle error
        console.log(response);
      });
  }

  private startClustering(): void {
    var data = new URLSearchParams();
    data.append("input_file", this.file);
    data.append("clustering_type", this.radioButton);
    data.append("num_clusters", this.clusterNumber.toString());
    data.append("reading_length", this.reading_length.toString());

    axios({
      method: "post",
      url: "clustering/",
      data: data,
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      timeout: 60000,
    })
      .then((response) => {
        this.$buefy.notification.open({
          message: "Clustering započet kao id:" + response.data,
          duration: 5000,
          type: "is-primary",
          pauseOnHover: true,
        });
      })
      .catch(() => {
        this.$buefy.notification.open({
          message: "Clustering nije uspio",
          duration: 5000,
          type: "is-danger",
          pauseOnHover: true,
        });
      });
  }
}
</script>

<style>
</style>