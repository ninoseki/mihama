<script setup lang="ts">
import { type PropType, computed } from 'vue'
import { RouterLink } from 'vue-router'

import type { VulnerabilityType } from '@/schemas'

const props = defineProps({
  vuln: {
    type: Object as PropType<VulnerabilityType>,
    required: true
  }
})

const packages = computed(() => {
  return (props.vuln.affected || [])
    .flatMap((a) => {
      return a.package
    })
    .filter((p): p is Exclude<typeof p, undefined> => p !== undefined)
})

const packageNames = computed<string[]>(() => {
  return packages.value.map((p) => `${p.ecosystem}/${p.name}`)
})

const truncatedPackageNames = computed(() => {
  if (packageNames.value.length <= 10) {
    return packageNames.value
  }

  return packageNames.value.slice(0, 9).concat(['...'])
})

const affectedVersions = computed<string[]>(() => {
  return (props.vuln.affected || []).flatMap((a) => a.versions || [])
})

const truncatedAffectedVersions = computed(() => {
  if (affectedVersions.value.length <= 10) {
    return affectedVersions.value
  }

  return affectedVersions.value.slice(0, 9).concat(['...'])
})

const ranges = computed(() => {
  return (props.vuln.affected || [])
    .flatMap((a) => {
      return a.ranges
    })
    .filter((p): p is Exclude<typeof p, undefined> => p !== undefined)
})

const events = computed(() => {
  return ranges.value.flatMap((r) => r.events)
})

const isFixed = computed(() => {
  return events.value.some((e) => e.fixed !== undefined)
})
</script>

<template>
  <tr>
    <td>
      <RouterLink :to="{ name: 'vuln', params: { id: vuln.id } }">{{ vuln.id }}</RouterLink>
    </td>
    <td>
      <div class="tags">
        <span class="tag" v-for="packageName in truncatedPackageNames" :key="packageName">{{
          packageName
        }}</span>
      </div>
    </td>
    <td>
      {{ vuln.summary }}
    </td>
    <td>
      <div class="tags">
        <span class="tag" v-for="version in truncatedAffectedVersions" :key="version">{{
          version
        }}</span>
      </div>
    </td>
    <td>
      {{ vuln.published }}
    </td>
    <td>
      <span class="tag is-success" v-if="isFixed">Fix available</span>
      <span class="tag is-danger" v-else>No fix available</span>
    </td>
  </tr>
</template>
