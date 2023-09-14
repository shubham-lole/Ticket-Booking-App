<template>
    <div>
        <div class="feed-section">
        <b-row align-h="center" justify="center" v-for="theater in Theaters['theaters']" :key="theater.TheaterID" class="theater-card" :id="'theater-' + theater.TheaterID">
          <b-card v-if="theater.TheaterID == theaterId">
            <template #header>
              <h5>{{ theater.Name }}</h5>
            </template>
            <b-card-text>
              <!-- Use a div with class="d-flex" to remove whitespace between b-row and b-col -->
              <div class="d-flex">
                <!-- Filter the shows array based on the current theater -->
                <b-col v-for="show in Shows['shows'].filter(show => show.Theaters.some(t => t.TheaterID === theater.TheaterID))" :key="show.ShowID" :id="'show-' + show.ShowID" cols="2">
                  <b-card class="show-card">
                    <template #header>
                      <h6>{{ show.Name }}</h6>
                    </template>
                    <!-- Show details can be displayed here -->
                    <b-card-text>
                      <p>Ticket Price: <b>Rs{{ show.TicketPrice }}/-</b></p>
                      <p>Rating: {{ show.Rating }}</p>
                      <label v-for="timing in show.Timings" :key="timing.TimingID">
                    <span v-if="timing.TheaterID == theater.TheaterID" class="mr-2">Timing:  {{ timing.Timing }}</span></label>
                      <!-- Add more show details here if needed -->
                    </b-card-text>
                    <!-- Add any other buttons or actions related to the show here -->
                    <!-- For example, you can add a "Book Show" button here -->
                
                    <template #footer>
                      <b-button-group v-for="timing in show.Timings"
                  :key="timing.TimingID" >
            
              <b-button
                v-if="timing.TheaterID == theater.TheaterID && Role == 'user'"
                @click="bookticket(show, timing)" variant="primary"
                :disabled="timing.isShowFull == true"
              >
              <p v-if="timing.TheaterID == theater.TheaterID && timing.isShowFull">Show Housefull</p>
              <p v-else> Book Show</p>
              </b-button>
            </b-button-group>
                      <b-button v-if="Role == 'admin'" @click="editShow(show)">Edit Show</b-button>
                    <b-button v-if="Role == 'admin'" variant="danger" @click="deleteShow(show.ShowID)">Delete Show</b-button>
                    </template>
                  </b-card>
                </b-col>
              </div>
            </b-card-text>
            <template #footer>
              <div v-if="Role == 'admin'">
                <b-button v-b-modal.modal-3 variant="primary" @click="editTheater(theater)">Edit Theater</b-button>&nbsp;
                <b-button variant="danger" @click="deleteTheater(theater.TheaterID)">Delete Theater</b-button>
              </div>
              </template>
          </b-card>
        </b-row>
      </div>
    </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
    name: "TheaterShows",
    data() {
        return {
            theaterId: "",
        };
    },
    computed: {
        ...mapGetters({ Theaters: "StateTheaters", Shows: "StateShows", Role: "StateRole" }),
    },
    created() {
        // Get the theater ID from query parameters
        this.theaterId = this.$route.params.theaterId || "";
    },
};
</script>
