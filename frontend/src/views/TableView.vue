<template>
  <div>
    <div v-if="tableData">
      <h3>表格資料</h3>
      <pre>{{ tableData }}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

export default {
  setup() {
    const route = useRoute()
    const tableData = ref(null)

    const fetchData = async (id) => {
      try {
        const response = await axios.get('http://localhost:8000/tables/test', {
          params: { id }
        })
        tableData.value = response.data
      } catch (error) {
        console.error('獲取資料時出錯：', error)
      }
    }

    onMounted(() => {
      const id = route.query.id
      if (id) {
        fetchData(id)
      } else {
        console.error('缺少 id 查詢參數')
      }
    })

    return {
      tableData
    }
  }
}
</script>

<style></style>
