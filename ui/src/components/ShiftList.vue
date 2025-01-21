<template>
  <div class="shift-list">
    <h3>Shifts for {{ planName }}</h3>
    <div class="areas-container">
      <div v-for="area in areas" :key="area.id" class="area-column">
        <h4>{{ area.name }}</h4>
        <div v-for="date in getDates()" :key="date" class="day-table">
          <h5>{{ formatDate(date) }}</h5>
          <vue-good-table
            :columns="getColumnsForDay()"
            :rows="getRowsForDay(date, area.id)"
            styleClass="vgt-table"
          >
            <template #table-row="props">
              <span v-if="props.column.field === 'assignment'" 
                    class="shift-bar"
                    :style="getShiftStyle(date, props.row.time)">
                <div class="assignment-slots" 
                     :style="`grid-template-columns: repeat(${props.row.capacity}, 1fr)`">
                  <div v-for="i in props.row.capacity" :key="i" class="slot">
                    {{ props.row.crew_members && props.row.crew_members[i-1] ? 
                       props.row.crew_members[i-1].name : '-' }}
                  </div>
                </div>
              </span>
              <span v-else>{{ props.row[props.column.field] }}</span>
            </template>
          </vue-good-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ShiftList',
  props: {
    planId: {
      type: Number,
      required: true
    },
    planName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      shifts: [],
      areas: []
    }
  },
  methods: {
    getDates() {
      return [...new Set(this.shifts.map(shift => 
        shift.start_time.split('T')[0]
      ))]
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', { 
        weekday: 'long', 
        month: 'short', 
        day: 'numeric' 
      })
    },
    getColumnsForDay() {
      return [
        { field: 'time', label: 'Time' },
        { field: 'assignment', label: 'Assignment' },
        { field: 'capacity', label: 'Capacity' }
      ]
    },
    getRowsForDay(date, areaId) {
      const dayShifts = this.shifts.filter(shift => 
        shift.start_time.split('T')[0] === date &&
        shift.area_id === areaId
      )

      return dayShifts.map(shift => ({
        time: `${shift.start_time.split('T')[1].substring(0, 5)} - ${shift.end_time.split('T')[1].substring(0, 5)}`,
        assignment: 'placeholder',
        capacity: shift.capacity,
        crew_members: shift.crew_members || []
      })).sort((a, b) => a.time.localeCompare(b.time))
    },
    getShiftStyle(date, timeSlot) {
      const shift = this.shifts.find(s => 
        s.start_time.split('T')[0] === date &&
        s.start_time.split('T')[1].startsWith(timeSlot.split(' - ')[0])
      )
      
      if (shift) {
        const startTime = new Date(shift.start_time)
        const endTime = new Date(shift.end_time)
        const duration = (endTime - startTime) / (1000 * 60 * 60)
        
        return {
          borderLeft: '4px solid #2196f3',
          height: `${Math.max(40, duration * 20)}px`,
          display: 'flex',
          alignItems: 'center',
          padding: '0 10px'
        }
      }
      return {}
    }
  },
  async created() {
    try {
      const [shiftsResponse, assignmentsResponse, crewResponse, areasResponse] = await Promise.all([
        axios.get(`http://localhost:8000/shifts/?plan_id=${this.planId}`),
        axios.get('http://localhost:8000/assignments/'),
        axios.get('http://localhost:8000/crew/'),
        axios.get('http://localhost:8000/areas/')
      ])
      
      const shifts = shiftsResponse.data
      const assignments = assignmentsResponse.data
      const crewMembers = crewResponse.data
      
      this.shifts = shifts.map(shift => {
        const shiftAssignments = assignments.filter(a => a.shift_id === shift.id)
        if (shiftAssignments.length > 0) {
          const assignedCrew = shiftAssignments
            .map(assignment => crewMembers.find(c => c.id === assignment.crew_member_id))
            .filter(Boolean)
          shift.crew_members = assignedCrew
        }
        return shift
      })
      this.areas = areasResponse.data
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }
}
</script>

<style scoped>
.shift-list {
  margin-top: 20px;
}
.areas-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 0 20px;
}
.area-column {
  min-width: 0;
}
.day-table {
  margin-bottom: 20px;
}
.vgt-table {
  font-size: 0.9em;
}
.shift-bar {
  border-radius: 4px;
  margin: 4px 0;
  transition: all 0.2s ease;
  width: 100%;
}
.assignment-slots {
  display: grid;
  gap: 4px;
  width: 100%;
}
.slot {
  padding: 2px;
  border: 1px dashed #ccc;
  border-radius: 4px;
  background-color: white;
  text-align: center;
  font-size: 0.8em;
}
</style>
