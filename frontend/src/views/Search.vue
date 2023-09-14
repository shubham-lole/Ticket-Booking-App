<template>
    <div class="search">
        <!-- Search Type Radio Buttons -->
        <div>
            <b-form-group>
                <b-form-radio-group v-model="searchType">
                    <b-form-radio value="theater">Search Theaters</b-form-radio>
                    <b-form-radio value="movie">Search Shows</b-form-radio>
                </b-form-radio-group>
            </b-form-group>
        </div>

        <!-- Theater Search Form -->
        <div v-if="searchType === 'theater'">
            <h3>Theater Search</h3>
            <b-form @submit.prevent="searchTheaters">
                <b-form-group label="Location Preference">
                    <b-form-input v-model="locationPreference"></b-form-input>
                </b-form-group>
                <b-button type="submit">Search Theaters</b-button>
            </b-form>
        </div>

        <!-- Movie Search Form -->
        <div v-else-if="searchType === 'movie'">
            <h3>Show Search</h3>
            <b-form @submit.prevent="searchShows">
                <b-form-group label="Tags">
                    <b-form-input v-model="tags"></b-form-input>
                </b-form-group>
                <b-button type="submit">Search Shows</b-button>
            </b-form>
        </div>

        <h3> Search Results </h3>

        <p v-if="showError" id="error">{{ er }}</p>

        <!-- Display search results for theaters -->
        <!--div v-if="theaterResults.length > 0"-->
        <div v-if="searchType === 'theater'">
            <b-row align-h="center" justify="center">
            <b-col cols="4" v-for="theater in theaterResults" :key="theater.TheaterID">
              <b-card>
                <template #header>
                  <h5>{{ theater.Name }}</h5>
                </template>
                <b-card-text>
                  <p>{{ theater.Place }}</p>
                  <p>Capacity: {{ theater.Capacity }}</p>
                </b-card-text>
                <b-button @click="goToTheater(theater.TheaterID)" variant="primary">Go to Theater</b-button>
              </b-card>
            </b-col>
          </b-row>
        </div>

        <!-- Display search results for movies -->
        <div v-if="searchType === 'movie'">
            <b-row align-h="center" justify="center">
                <b-col cols="4" v-for="movie in showResults" :key="movie.ShowID">
                  <b-card>
                    <template #header>
                      <h5>{{ movie.Name }}</h5>
                    </template>
                    <b-card-text>
                      <p>Ticket Price: Rs{{ movie.TicketPrice }}/-</p>
                      <p>Rating: {{ movie.Rating }}</p>
                      <p>Tags: {{ movie.Tags }}</p>
                    </b-card-text>
                    <b-button @click="goToShow(movie.ShowID)" variant="primary">Go to Show</b-button>
                  </b-card>
                </b-col>
              </b-row>
        </div>
    </div>
</template>

<script>
import { mapActions,mapGetters } from 'vuex';
//import TheaterShows from './TheaterShows.vue';

export default {
    name: "Search",
    data() {
        return {
            searchType: "theater",
            locationPreference: "",
            tags: "",
            rating: "",
            theaterResults: [],
            showResults: [],
            er: [],
            showError: false
        };
    },
    computed: {
        ...mapGetters({ Theaters: "StateTheaters", Shows: "StateShows" }),
    },
    methods: {
        ...mapActions({ SearchTheater: "SearchTheater", SearchShow: "SearchShow" }),
        async searchTheaters() {
            try {
                const response = await this.$store.dispatch("SearchTheater", this.locationPreference);
                this.theaterResults = response.theaters;
                console.log(response.theaters);
            } catch (error) {
                this.theaterResults = [];
                console.log(error);
                this.showError = true;
                this.er = error;
            }
        },
        async searchShows() {
            try {
                const response = await this.$store.dispatch("SearchShow", this.tags);
                console.log(response);
                this.showResults = response.shows;
            } catch (error) {
                this.showResults = [];
                console.log(error);
                this.showError = true;
                this.er = error;
            }
        },
        goToTheater(theaterId) {
            this.$router.push({name: "TheaterShows", params: {theaterId: theaterId}});
        },
        goToShow(showId) {
            const targetId = "show-" + showId;

            // Append the show ID to the URL as a hash
            // This will create a URL like /#show-1 for show with ID 1
            this.$router.push({ name: "Home" });

            // Use $nextTick to wait for the next update cycle
            this.$nextTick(() => {
                // Scroll to the show section with the given ID
                const showElement = document.getElementById(targetId);
                if (showElement) {
                    showElement.scrollIntoView({ behavior: "smooth" });
                }
            });
        },
    },
};
</script>

<style>
/* Add your CSS styles here */
</style>
