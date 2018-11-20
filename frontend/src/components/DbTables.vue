<template>
  <div class="db-tables" v-if="tablesExist()">
    <div class="header d-flex justify-content-between align-items-center">
      <h5>Tables</h5>
      <b-button-group variant="info" class="align-self-end">
        <b-button variant="success" v-b-tooltip.hover title="Saves the tables to localStorage" @click="saveTables()">Save</b-button>
        <b-button variant="info" v-b-tooltip.hover title="Restores the tables from localStorage (this is done automatically on mount)" @click="loadTables()">Restore</b-button>
        <b-button variant="outline-danger" v-b-tooltip.hover title="Deletes the tables from localStorage" @click="deleteTables()">Delete</b-button>
      </b-button-group>
    </div>
    <b-card no-body>
      <b-tabs card nav-wrapper-class="small" v-model="tabIndex">
        <b-tab small="true"
          v-for="(table, i) in tables" :key="i"
          v-bind="{ title: `${table.name}`, }" active>
          <b-table small striped hover :fields="table.headers" :items="table.rows"></b-table>
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'DbTables',
  mounted() {
    this.checkAndRestoreFromLocal()
  },
  computed: {
    ...mapGetters('risks', {
      risks: 'availableRisks',
      selectedRisk: 'selectedRisk'
    }),
    ...mapGetters('database', {
      tables: 'tables',
    }),
    tabIndex: {
      get() {
        return this.$store.state.database.tabIndex
      },
      set(value) {
        this.$store.commit('database/setTabIndex', value)
      }
    }
  },
  methods: {
    linkClass (idx) {
      if (this.tabIndex === idx) {
        return ['bg-primary', 'text-light']
      } else {
        return ['bg-light', 'text-info']
      }
    },
    createTables() {
      for(let r of this.risks) {
        this.$store.dispatch('database/createTable', r)
      }
    },
    tablesExist() {
      return this.tables ? this.tables.length > 0 : false
    },
    saveTables() {
      this.$store.dispatch('database/saveTables')
    },
    loadTables() {
      this.$store.dispatch('database/restoreTables')
    },
    deleteTables() {
      this.$store.dispatch('database/deleteTables')
    },
    checkAndRestoreFromLocal() {
      let exists = localStorage.tables ? localStorage.tables.length > 0 : false
      if(exists) {
        this.$store.commit('log/write', 'Found tables stored in localStorage, restoring...')
        this.$store.dispatch('database/restoreTables')
      }
    }
  },
  watch: {
    selectedRisk: function() {
      if (this.selectedRisk !== null) {
        this.$store.dispatch('database/createTable', this.selectedRisk)
      }
    },
  }
}
</script>

<style scoped>
.db-tables {
  order: 2;
  /* max-height: 35h;
  height: 35vh; */
  padding-top: 1em;
}
@media (min-width: 760px) {
}
</style>
