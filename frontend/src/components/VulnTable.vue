<script setup lang="ts">
import type { PropType } from 'vue'

import VulnRow from '@/components/VulnRow.vue'
import type { VulnerabilityType } from '@/schemas'

defineProps({
  vulns: {
    type: Array as PropType<VulnerabilityType[]>,
    required: true
  }
})
</script>

<template>
  <table class="table is-fullwidth" v-if="vulns.length">
    <thead>
      <tr>
        <th>ID</th>
        <th>Packages</th>
        <th>Summary</th>
        <th>Affected versions</th>
        <th>Published</th>
        <th>Fix</th>
      </tr>
    </thead>
    <tbody>
      <VulnRow :vuln="vuln" v-for="vuln in vulns" :key="vuln.id" />
    </tbody>
  </table>
  <p class="has-text-centered" v-else>No results</p>
</template>
