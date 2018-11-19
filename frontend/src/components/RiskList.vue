<template>
  <div class="tablist risk-list">
    <div class="header d-flex justify-content-between align-items-center">
      <h5>Available risk list</h5>
      <b-btn @click="restoreOriginalRisks()"><small>{{ this.risks.length === 0 ? 'Create samples' : 'Restore samples' }}</small></b-btn>
    </div>
    <div v-for="(risk, i) in risks" v-bind:key="i">
      <b-card  no-body class="mb-1" role="tablist">
        <b-card-header class="p-1 d-flex justify-content-between align-items-center" header-tag="header" role="tab">
            <b-btn 
              block
              class="d-flex justify-content-between align-items-center"
              @click="clickRisk(risk, i)"
              :class="showCollapse[i] ? 'collapsed' : null" 
              v-bind="{ 'aria-controls': `risk-${i}` }" 
              :aria-expanded="showCollapse[i] ? 'true' : 'false'"
              variant="default">
              {{ risk.name }}<b-btn-close @click="deleteRisk(risk)" variant="default"></b-btn-close>
            </b-btn>
        </b-card-header>
        <b-collapse v-bind="{ id: `risk-${i}`, visible: showCollapse[i] }" v-model="showCollapse[i]" accordion="risk-accordion" role="tabpanel">
          <b-card-body>
            <p class="card-text">
              {{ risk.description }}
            </p>
          </b-card-body>
        </b-collapse>
      </b-card>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'RiskList',
  data () {
    return {
      showCollapse: []
    }
  },
  mounted() {
    this.getRisks()
    // eslint-disable-next-line
    this.showCollapse = this.risks.map((r, i) => false)
  },
  computed: {
    ...mapGetters('risks', {
      risks: 'availableRisks',
      selectedRisk: 'selectedRisk',
    }),
  },
  methods: {
    getRisks: function() {
      this.$store.dispatch('risks/getRisks')
    },
    selectRisk: function(risk) {
      this.$store.dispatch('risks/selectRisk', risk)
    },
    deSelectRisk: function() {
      this.$store.dispatch('risks/deSelectRisk')
    },
    restoreOriginalRisks: function() {
      this.$store.dispatch('risks/restoreOriginalRisks')
    },
    deleteRisk: function(risk) {
      this.$store.dispatch('risks/deleteRisk', risk)
    },
    clickRisk: function(risk, i) {
      this.showCollapse = this.showCollapse.map((b, j) => i === j ? !this.showCollapse[i] : false)
      if(this.selectedRisk !== null && this.selectedRisk.slug === risk.slug) {
        this.deSelectRisk(risk)
      } else {
        this.selectRisk(risk)
      }
    }
  }
}
</script>

<style scoped>
.risk-list {
  order: 2;
  max-height: 35vh;
  height: 35vh;
  overflow-y: scroll;
}
@media (min-width: 760px) {
  .risk-list {
    grid-row: 1 / 2;
    grid-column: 2 / 3;
  }
}
</style>
