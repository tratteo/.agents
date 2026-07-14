---
name: nuxt-4-preferred
description: Build Nuxt 4 applications with preferred conventions - Composition API, TypeScript, Nuxt UI v4, Pinia, VueUse. Use this skill whenever the user wants to create pages, components, composables, stores, or set up server API routes in a Nuxt 4 project.
---

# Nuxt 4 Preferred Conventions

This skill helps build Nuxt 4 applications following your preferred conventions.

## Your Preferences
- **Nuxt 4.x** with latest features
- **Composition API** with `<script setup>` syntax
- **TypeScript** for all components, composables, and stores
- **Nuxt UI v4** for UI components
- **Pinia** for state management
- **VueUse** composables for common patterns
- **File-based routing** (pages/ directory)
- **Server routes** for API endpoints
- **Bun** as package manager

## MCP Server for Nuxt UI

Use the MCP server to browse Nuxt UI documentation:

```
resource://nuxt-ui/components - Browse all available components
resource://nuxt-ui/composables - Browse all available composables
resource://nuxt-ui/examples - Browse code examples
resource://nuxt-ui/templates - Browse project templates
resource://nuxt-ui/documentation-pages - Browse documentation
```

Always query these resources when you need to find the right Nuxt UI component or check its API.

## Scaffolding New Projects

When creating a new Nuxt project from scratch:

1. Create `app/app.vue` with u-app and nuxt-layout:
```vue
<template>
  <u-app>
    <nuxt-layout>
      <nuxt-page />
    </nuxt-layout>
  </u-app>
</template>
```

2. Create `app/layouts/default.vue`:
```vue
<template>
  <div class="min-h-screen bg-background">
    <slot />
  </div>
</template>
```

3. Create `assets/css/main.css`:
```css
@import "tailwindcss";
@import "@nuxt/ui";
```

4. Add to `nuxt.config.ts` css array:
```ts
export default defineNuxtConfig({
  css: ['~/assets/css/main.css']
})
```

## Naming Conventions

- **Pages**: Use kebab-case in `app/pages/` (e.g., `my-page.vue`, `about-us.vue`)
- **Components**: Use snake_case in `app/components/` (e.g., `my_component.vue`)
- **Composables**: Use snake_case in `app/composables/` (e.g., `use_feature.ts`)
- **Stores**: Use snake_case in `app/composables/stores/` (e.g., `config_store.ts`)

## When Creating Pages

Create files in `app/pages/` directory with kebab-case names.

```vue
<script setup lang="ts">
const route = useRoute()
const configStore = useConfigStore()
</script>

<template>
  <div class="p-4">
    <h1 class="text-lg font-semibold">Page Title</h1>
  </div>
</template>
```

**Important**: Do NOT add imports for auto-imported elements (useRoute, useRouter, $fetch, useNuxtApp, etc.).

## When Creating Components

Create files in `app/components/` with snake_case names.

```vue
<script setup lang="ts">
interface Props {
  title: string
  count?: number
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
})

const emit = defineEmits<{
  update: [value: number]
}>()
</script>

<template>
  <u-button @click="emit('update', props.count + 1)">
    {{ title }}: {{ count }}
  </u-button>
</template>
```

**Use Nuxt UI First**: ALWAYS prefer Nuxt UI components over creating custom ones. Only create custom components if explicitly instructed or if Nuxt UI cannot achieve the required functionality.

## Form Layout with u-form-field

Use `u-form-field` for any label + element combination, not just forms:

```vue
<template>
  <div class="space-y-4">
    <u-form-field label="Name">
      <u-input v-model="name" />
    </u-form-field>
    
    <u-form-field label="Email">
      <u-input v-model="email" type="email" />
    </u-form-field>
    
    <u-form-field label="Description">
      <u-textarea v-model="description" />
    </u-form-field>
  </div>
</template>
```

## Nuxt UI Theming - Use Default Colors

Always use Nuxt UI theme colors instead of custom Tailwind colors:

| Instead of... | Use... |
|---------------|--------|
| text-red-500 | text-error |
| text-green-500 | text-success |
| text-blue-500 | text-info |
| text-yellow-500 | text-warning |
| bg-gray-800 | bg-elevated |
| bg-gray-100 | bg-disabled |
| bg-white | bg-default |
| text-gray-500 | text-muted |

**Do NOT modify the `ui` prop of Nuxt UI components** unless explicitly necessary. Keep the default styling for consistency.

## Using VueUse

Before creating a custom composable, ALWAYS check if VueUse already provides it:

- `useStorage` - localStorage reactive
- `useNetwork` - network status
- `useMouse` / `useMouseInElement` - mouse position
- `useDebounce` / `useThrottleFn` - timing
- `useAsyncData` / `useFetch` - data fetching with SSR
- `useElementSize` - element dimensions
- `useWindowSize` - window dimensions

When creating custom composables, prefer wrapping/combining existing VueUse composables:

```typescript
export const useCustomFeature = () => {
  const storage = useStorage('my-key', 'default')
  const { width } = useElementSize(targetRef)
  
  return { storage, width }
}
```

## When Creating Composables

Create files in `app/composables/` with snake_case names and `.ts` extension.

```typescript
export const useDataFetcher = () => {
  const data = ref<string | null>(null)
  const loading = ref(false)

  const fetchData = async () => {
    loading.value = true
    try {
      const result = await $fetch('/api/endpoint')
      data.value = result as string
    } finally {
      loading.value = false
    }
  }

  return {
    data: readonly(data),
    loading: readonly(loading),
    fetchData
  }
}
```

**Do NOT add imports** for auto-imported elements: `ref`, `computed`, `watch`, `useRoute`, `useRouter`, `useNuxtApp`, `$fetch`, `useAsyncData`, `useFetch`, etc.

## When Creating Pinia Stores

Create files in `app/composables/stores/` with snake_case names and `.ts` extension.

```typescript
import { defineStore } from 'pinia'

export const useConfigStore = defineStore('config', () => {
  const items = ref<string[]>([])
  const selected = ref<string | null>(null)

  const addItem = (item: string) => {
    items.value.push(item)
  }

  const selectItem = (item: string | null) => {
    selected.value = item
  }

  return {
    items: readonly(items),
    selected: readonly(selected),
    addItem,
    selectItem
  }
})
```

## When Creating Server API Routes

Create files in `app/server/api/` with kebab-case names and `.ts` extension.

```typescript
export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  
  return {
    success: true,
    data: []
  }
})
```

## File Structure Reference

```
app/
├── app.vue                    # Root with UApp + NuxtLayout
├── pages/
│   ├── index.vue              # kebab-case
│   └── my-page.vue            # kebab-case
├── components/
│   ├── my_component.vue       # snake_case
│   └── ui/
├── composables/
│   ├── use_feature.ts          # camelCase
│   └── stores/
│       └── config_store.ts    # snake_case
├── layouts/
│   └── default.vue
├── server/
│   └── api/
│       └── my-endpoint.ts     # kebab-case
└── types/
assets/
└── css/
    └── main.css
```

## TypeScript Conventions

- Always use `lang="ts"` in `<script setup>`
- Define interfaces for props and emits
- Use `readonly` for computed/read-only refs
- Use `$fetch` for API calls (auto-imported)

## Important Notes

- Nuxt 4 auto-imports composables, components, and utilities
- Store files go in `app/composables/stores/` not `app/stores/`
- Use MCP resources to browse Nuxt UI components before implementing
- Keep all Nuxt UI components at their default styling
- Use theme colors (text-error, bg-elevated, etc.) instead of custom colors