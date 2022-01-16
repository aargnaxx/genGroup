<template>
  <section>
    <b-field>
      <b-upload v-model="dropFiles" multiple drag-drop>
        <section class="section">
          <div class="content has-text-centered">
            <p>
              <b-icon icon="upload" size="is-large"> </b-icon>
            </p>
            <p>Drop your files here or click to upload</p>
          </div>
        </section>
      </b-upload>
    </b-field>
    <div class="tags">
      <span
        v-for="(file, index) in dropFiles"
        :key="index"
        class="tag is-primary"
      >
        {{ file.name }}
        <button
          class="delete is-small"
          type="button"
          @click="deleteDropFile(index)"
        ></button>
      </span>
    </div>
    <button @click="Upload">Upload</button>
  </section>
</template>

<script lang="ts">
import { Component, Model, Vue } from "vue-property-decorator";
import axios from "axios";

@Component
export default class Upload extends Vue {
  @Model() private dropFiles: File[] = [];
  @Model() private checkedRows: any[] = [];

  private Upload(): void {
    const loadingComponent = this.$buefy.loading.open({
      container: null,
    });
    
    this.dropFiles.forEach( async (element) => {
      var bodyFormData = new FormData();
      bodyFormData.append("name", element.name);
      bodyFormData.append("file", element);

      await axios({
        method: "post",
        url: "http://localhost:8001/files/",
        data: bodyFormData,
        headers: { "Content-Type": "multipart/form-data" },
      })
        .then((response) => {
          this.$buefy.notification.open({
            message: element.name + ` uploaded succesfully`,
            duration: 5000,
            progressBar: true,
            type: "is-primary",
            pauseOnHover: true,
          });
          //handle success
          console.log(response);
        })
        .catch((response) => {
          this.$buefy.notification.open({
            message: `Upload fail`,
            duration: 5000,
            progressBar: true,
            type: "is-danger",
            pauseOnHover: true,
          });
          console.log(response);
        });
    });
    loadingComponent.close()
    this.dropFiles= [];
  }

  deleteDropFile(index: number) {
    this.dropFiles.splice(index, 1);
  }
}
</script>

<style>
</style>