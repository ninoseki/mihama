/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

const mode = process.env.NODE_ENV === 'production' ? 'error' : 'warn'

module.exports = {
  root: true,
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier/skip-formatting'
  ],
  plugins: ['simple-import-sort'],
  rules: {
    'no-console': mode,
    'no-debugger': mode,
    'simple-import-sort/imports': mode,
    'simple-import-sort/exports': mode
  },
  parserOptions: {
    ecmaVersion: 'latest'
  }
}
