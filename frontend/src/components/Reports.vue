<template>
  <div class="section">
    <div class="columns">
      <div class="column">
        <b-field label="Vrsta izvještaja">
          <b-select
            placeholder="Odaberite izvještaj"
            expanded
            v-model="reportType"
          >
            <option value="0">Prva vrsta izvještaja</option>
            <option value="1">Druga vrsta izvještaja</option>
            <option value="2">Usporedba s drugom datotekom</option>
          </b-select>
        </b-field>
      </div>
      <div class="column">
        <b-field label="Rezultat">
          <b-select placeholder="Odaberite rezultat" expanded v-model="file1">
            <option value="path1">Rezultat1</option>
            <option value="path2">Rezultat2</option>
            <option value="path2">Rezultat3</option>
            <option value="path2">Rezultat4</option>
          </b-select> </b-field
        ><b-field v-if="reportType == 2" label="Datoteka za usporedbu">
          <b-select placeholder="Odaberite datoteku" expanded v-model="file2">
            <option value="path1">Datoteka1</option>
            <option value="path2">Datoteka2</option>
            <option value="path2">Datoteka3</option>
            <option value="path2">Datoteka4</option>
          </b-select>
        </b-field>
      </div>
    </div>
    <b-button type="is-primary is-light">Prikaži izvještaj</b-button>
  </div>
</template>


<script lang="ts">
import { Component, Model, Vue } from "vue-property-decorator";

@Component
export default class Reports extends Vue {
  @Model() private dropFiles: string[] = [];
  @Model() public reportType = 0;

  @Model() private data: any[] = [
    {
      path: "abc",
    },
    {
      path: "abc",
    },
    {
      path: "abc",
    },
    {
      path: "abc",
    },
  ];
}
</script>

<style>
</style>