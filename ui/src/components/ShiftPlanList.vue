<template>
  <div class="shift-plans">
    <h2>Shift Plans</h2>
    <div v-for="plan in plans" 
         :key="plan.id" 
         class="plan-item"
         @click="selectPlan(plan)">
      <h3>{{ plan.name }}</h3>
      <span class="status">Status: {{ plan.status }}</span>
    </div>
    
    <ShiftList v-if="selectedPlan" 
               :planId="selectedPlan.id"
               :planName="selectedPlan.name" />
  </div>
</template>

<script>
import axios from 'axios'
import ShiftList from './ShiftList.vue'

export default {
  name: 'ShiftPlanList',
  components: {
    ShiftList
  },
  data() {
    return {
      plans: [],
      selectedPlan: null
    }
  },
  methods: {
    selectPlan(plan) {
      if (this.selectedPlan && this.selectedPlan.id === plan.id) {
        this.selectedPlan = null
      } else {
        this.selectedPlan = plan
      }
    }
  },
  async created() {
    try {
      console.log('ShiftPlanList component created')
      const response = await axios.get('http://localhost:8000/plans/')
      console.log('Plans received:', response.data)
      this.plans = response.data
    } catch (error) {
      console.error('Error fetching plans:', error)
    }
  }
}
</script>

<style scoped>
.shift-plans {
  padding: 20px;
}
.plan-item {
  border: 1px solid #ddd;
  margin: 10px 0;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
