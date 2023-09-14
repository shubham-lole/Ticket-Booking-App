<template>
    <div>
        <br>
        <h1>Export</h1>
        <br><br>
        <b-form @submit.prevent="exportcsv">
          <b-form-group label="Select Theater:" label-for="theaterSelect" style="font-size:larger;">
            <b-form-select v-model="theaterId" :options="theaterOptions" id="theaterSelect"></b-form-select>
          </b-form-group>
      
          <div v-if="error" class="alert alert-danger">{{ error }}</div>

          <b-button type="submit" variant="primary">Export CSV</b-button>
        </b-form>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios'

export default {
    name: "Export",
    data() {
        return {
            theaterId: "",
            error: "",
        }
    },
    computed: {
        ...mapGetters({ Theaters: 'StateTheaters', Token: 'StateToken' }),
        theaterOptions() {
            return this.Theaters.theaters.map((theater) => ({
                value: theater.TheaterID,
                text: theater.Name
            }));
        }
    },
    methods: {
        exportcsv() {
            try {
                const response = axios.get(`/api/export/${this.theaterId}`, {
                    headers: {
                        Authorization: `Bearer ${this.Token}`,
                    },
                }).then((response) => {
                    console.log(response)
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', 'theater_data.csv');
                    document.body.appendChild(link);
                    link.click();
                })
                console.log(response)
                return response;
            }
            catch (error) {
                console.log(error)
            }
        },
    },
}
</script>

<style></style>
