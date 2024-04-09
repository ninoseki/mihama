<script setup lang="ts">
import markdownit from 'markdown-it'
import { type PropType, computed, onMounted, ref } from 'vue'

import AffectedPackage from '@/components/AffectedPackage.vue'
import { type AffectedType, type VulnerabilityType } from '@/schemas'

const props = defineProps({
  vuln: {
    type: Object as PropType<VulnerabilityType>,
    required: true
  }
})

const markdownDetails = computed(() => {
  if (!props.vuln.details) {
    return undefined
  }

  const md = markdownit()
  return md.render(props.vuln.details)
})

const affected = computed(() => {
  return (props.vuln.affected || []).filter((a) => a.package)
})

const selectedAffected = ref<AffectedType>()

const isSelectedAffected = (a: AffectedType): boolean => {
  return JSON.stringify(a) === JSON.stringify(selectedAffected.value)
}

const selectAffected = (a: AffectedType) => {
  selectedAffected.value = a
}

onMounted(() => {
  if (affected.value.length > 0) {
    selectedAffected.value = affected.value[0]
  }
})
</script>

<template>
  <h2 class="is-size-2">{{ vuln.id }}</h2>
  <table class="table is-fullwidth is-completely-borderless">
    <tr v-if="vuln.related">
      <th>Related</th>
      <td>
        <ul>
          <li v-for="r in vuln.related || []" :key="r">{{ r }}</li>
        </ul>
      </td>
    </tr>
    <tr v-if="vuln.published">
      <th>Published</th>
      <td>
        {{ vuln.published }}
      </td>
    </tr>
    <tr>
      <th>Modified</th>
      <td>
        {{ vuln.modified }}
      </td>
    </tr>
    <tr v-if="markdownDetails">
      <th>Details</th>
      <td class="content" v-html="markdownDetails"></td>
    </tr>
    <tr v-if="vuln.references">
      <th>References</th>
      <td>
        <ul>
          <li v-for="r in vuln.references || []" :key="r.url">
            <a target="_blank" :href="r.url">{{ r.url }}</a>
          </li>
        </ul>
      </td>
    </tr>
  </table>
  <h3 class="is-size-3">Affected packages</h3>
  <div class="tabs">
    <ul>
      <li
        :class="{ 'is-active': isSelectedAffected(a) }"
        v-for="(a, index) in affected"
        :key="index"
      >
        <a @click="selectAffected(a)">
          <strong>{{ a.package?.ecosystem }}</strong
          >: {{ a.package?.name }}
        </a>
      </li>
    </ul>
  </div>
  <div v-for="(a, index) in affected" :key="index">
    <AffectedPackage :affected="a" v-if="isSelectedAffected(a)" />
  </div>
</template>
