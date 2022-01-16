<template>
  <div>
    <section>
      <b-field label="Datoteka za analizu">
        <b-select placeholder="Odaberi datoteku" expanded v-model="file1">
          <option v-for="(option, i) in files" :value="option" :key="i">
            {{ option }}
          </option>
        </b-select>
      </b-field>
      <b-field label="Očekivani rezultat">
        <b-select placeholder="Odaberi datoteku" expanded v-model="file2">
          <option v-for="(option, i) in files" :value="option" :key="i">
            {{ option }}
          </option>
        </b-select>
      </b-field>
      <button @click="Preprocess">Preprocess</button>
    </section>

    <!-- <canvas id="c" width="550" height="160"></canvas> -->
    <section v-if="dataReady">
      <table style="display: inline-table">
        <tr>
          <th></th>
          <th v-for="(name, i) in sequenceNames" :key="i">{{ name }}</th>
        </tr>
        <tr v-for="(name1, i) in sequenceNames" :key="i">
          <td>{{ name1 }}</td>
          <td v-for="(name2, j) in sequenceNames" :key="j">
            {{ dict[name1 + name2] }}
          </td>
        </tr>
      </table>

      <TestChart :chartdata="chartdata" :options="options" />
      <!-- <line-chart :chartdata="chartdata" :options="options" v-for="(sequence, i) in sequenceDistances" :key="i"/> -->
      <line-chart :chartdata="lineChartData" :options="lineChartOptions" />
    </section>
  </div>
</template>

<script lang="ts">
import { Component, Model, Vue } from "vue-property-decorator";
import axios from "axios";
import TestChart from "../components/TestChart.vue";
import LineChart from "../components/LineChart.vue";

@Component({
  components: {
    TestChart,
    LineChart,
  },
})
export default class Preprocessing extends Vue {
  @Model() private files: string[] = [];
  @Model() private file1 = "";
  @Model() private file2 = "";
  @Model() private dataPoints: any[] = [];
  @Model() private sequenceNames: string[] = [];
  @Model() private dataReady = false;
  @Model() private dict: any = {};
  @Model() private chartdata: any = null;
  @Model() private options: any = {};
  @Model() private lineChartData: any = null;
  @Model() private lineChartOptions: any = null;

  private colorScheme = [
    "#1abc9c",
    "#3498db",
    "#9b59b6",
    "#34495e",
    "#f1c40f",
    "#e74c3c",
    "#34e7e4",
    "#ffdd59",
    "#808e9b",
  ];

  private Preprocess(): void {
    const loadingComponent = this.$buefy.loading.open({
      container: null,
    });
    this.dataReady = false;
    var data = new URLSearchParams();
    data.append("file_to_analyze", this.file1);
    data.append("result_file", this.file2);

    axios({
      method: "post",
      url: "http://localhost:8001/preprocess/",
      data: data,
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      timeout: 60000,
    })
      .then((response) => {
        //handle success
        //         console.log(response);
        //         var histogramData: any = [];
        //         for (const [key, value] of Object.entries(
        //           response.data.sequence_lengths
        //         )) {
        //           histogramData.push({ aCount: value, aLength: key });
        //           this.dataPoints.push(value)
        //         }
        //         console.log(histogramData);
        //         var c = document.getElementById("c");
        // var ctx = (c as any).getContext("2d");
        // ctx.beginPath();
        // ctx.moveTo(10,0)
        // ctx.lineTo(10,150);
        // ctx.lineTo(550,150);
        // ctx.stroke();
        var a: string[] = [];
        response.data.distances_between_results.forEach((element: any) => {
          a.push(element[0]);
          this.dict[element[0] + element[1]] = element[2];
        });
        this.sequenceNames = a.filter((v, i, a) => a.indexOf(v) === i);

        var lengths = response.data.sequence_lengths;
        var maxLength = Math.max.apply(
          null,
          Object.keys(lengths).map((x) => Number(x))
        );

        var minLength = Math.min.apply(
          null,
          Object.keys(lengths).map((x) => Number(x))
        );

        this.chartdata = {
          labels: [],
          datasets: [
            {
              label: "Duljina",
              backgroundColor: "#f87979",
              data: [],
            },
          ],
        };
        for (let index = minLength; index < maxLength; index++) {
          if (lengths[index] != null) {
            this.chartdata.datasets[0].data.push(lengths[index]);
          } else {
            this.chartdata.datasets[0].data.push(0);
          }
          this.chartdata.labels.push(index);
        }

        this.options = {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            yAxes: [
              {
                scaleLabel: {
                  display: true,
                  labelString: "Broj pojavljivanja",
                },
              },
            ],
            xAxes: [
              {
                scaleLabel: {
                  display: true,
                  labelString: "Duljina sekvence",
                },
                barPercentage: 1,
                categoryPercentage: 1,
              },
            ],
          },
        };

        var xa =
          response.data.distances[Object.keys(response.data.distances)[0]]
            .length;

        console.log(xa);
        var j = 0;
        this.lineChartData = {
          labels: [...Array(xa).keys()],
          datasets: Object.keys(response.data.distances).map((x: any) => {
            var d = {
              label: x,
              backgroundColor: this.colorScheme[j],
              borderColor: this.colorScheme[j],
              data: response.data.distances[x],
              fill: false,
            };
            j++;
            return d;
          }),
        };

        console.log(this.lineChartData);

        this.lineChartOptions = {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            yAxes: [
              {
                scaleLabel: {
                  display: true,
                  labelString: "Očitanja kumulativno",
                },
              },
            ],
            xAxes: [
              {
                scaleLabel: {
                  display: true,
                  labelString: "Udaljenost",
                },
              },
            ],
          },
        };

        this.dataReady = true;
      })
      .catch(function (response) {
        //handle error
        console.log(response);
      })
      .finally(() => loadingComponent.close());
  }

  mounted(): void {
    axios({
      method: "get",
      url: "http://localhost:8001/files/",
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
}
</script>

<style>
table,
th,
td {
  border: 1px solid black;
}
</style>