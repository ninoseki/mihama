<script setup lang="ts">
import { useDark, useToggle } from '@vueuse/core'
import { RouterLink } from 'vue-router'

const isDark = useDark({
  selector: 'html',
  valueDark: 'theme-dark',
  valueLight: 'theme-light'
})
const toggleDark = useToggle(isDark)
</script>

<template>
  <nav role="navigation" aria-label="main navigation" class="navbar is-fixed-top">
    <div class="navbar-brand">
      <a class="navbar-item"><h1 class="title">Mihama</h1></a>
    </div>
    <div class="navbar-menu">
      <div class="navbar-start">
        <RouterLink class="navbar-item" to="/">Home</RouterLink>
        <a class="navbar-item"><a href="/redoc" target="_blank" class="navbar-item">API</a></a>
        <a class="navbar-item"
          ><a href="https://github.com/ninoseki/mihama" target="_blank" class="navbar-item"
            >GitHub</a
          ></a
        >
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <span class="icon" @click="toggleDark()">
            <font-awesome-icon :icon="isDark ? 'moon' : 'sun'"></font-awesome-icon>
          </span>
        </div>
      </div>
    </div>
  </nav>
</template>
