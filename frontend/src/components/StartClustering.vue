<template>
  <div>
    <b-field>
      <b-radio-button
        v-model="radioButton"
        native-value="reg"
        type="is-danger is-light is-outlined"
        acti
      >
        <span>Običan clustering</span>
      </b-radio-button>

      <b-radio-button
        v-model="radioButton"
        native-value="notreg"
        type="is-success is-light is-outlined"
      >
        <span>Određen broj clustera</span>
      </b-radio-button>
    </b-field>
    <b-field v-if="radioButton == 'notreg'">
      <b-field label="Broj klustera">
        <b-numberinput v-model="number"></b-numberinput>
      </b-field>
    </b-field>
    <b-field label="Datoteka">
      <b-select placeholder="Odaberi datoteku" expanded v-model="file">
        <option v-for="(option, i) in files" :value="option" :key="i">
          {{ option }}
        </option>
      </b-select>
    </b-field>
    <b-button type="is-primary">Započni</b-button>
  </div>
</template>

<script lang="ts">
import { Component, Model, Vue } from "vue-property-decorator";
import axios from "axios";

@Component
export default class StartClustering extends Vue {
  @Model() private dropFiles: string[] = [];
  @Model() private radioButton = "reg";
  @Model() private file = "";

  private files: string[] = [];

  mounted(): void{

    axios({
        method: "get",
        url: "http://localhost:8001/files/",
      })
        .then(response =>{
          this.files = response.data.files;
          console.log(response);
        })
        .catch(function (response) {
          //handle error
          console.log(response);
        });
  }
}
</script>

<style>
</style>