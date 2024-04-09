<script setup lang="ts">
import { RouterView } from 'vue-router'

import Navbar from '@/components/NavbarItem.vue'
</script>

<template>
  <Navbar />
  <section class="section is-medium">
    <div class="container fluid">
      <RouterView />
    </div>
  </section>
</template>
