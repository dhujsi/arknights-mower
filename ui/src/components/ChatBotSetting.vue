<script setup>
import { computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { storeToRefs } from 'pinia'

const store = useConfigStore()
const { ai_key, ai_type, ai_base_url, ai_model } = storeToRefs(store)
const type_options = [
  { label: 'Deepseek', value: 'deepseek' },
  { label: 'Deepseek 深度推理', value: 'deepseek_reasoner' },
  { label: 'OpenAI-Compatible', value: 'openai_compatible' }
]
const isOpenAICompatible = computed(() => ai_type.value === 'openai_compatible')
</script>
<template>
  <n-card>
    <template #header>
      <div class="card-title">本地 AI 助手</div>
      <help-text
        ><div>支持 Deepseek 和 OpenAI-Compatible 接口</div>
        <div>
          Deepseek 密钥请前往
          <a href="https://platform.deepseek.com/api_keys" target="_blank">Deepseek 官网</a> 获取，
          充值 1 元即可使用很久
        </div>
        <div>OpenAI-Compatible 可以留空 Base URL 以使用官方 OpenAI 接口。</div>
      </help-text>
    </template>
    <n-form label-placement="left" label-width="auto">
      <n-form-item label="AI 类型">
        <n-select v-model:value="ai_type" :options="type_options" />
      </n-form-item>
      <n-form-item label="API 密钥">
        <n-input
          type="password"
          v-model:value="ai_key"
          placeholder="请输入 API 密钥"
          show-password-on="click"
        />
      </n-form-item>
      <n-form-item v-if="isOpenAICompatible" label="Base URL">
        <n-input v-model:value="ai_base_url" placeholder="https://api.openai.com/v1" />
      </n-form-item>
      <n-form-item v-if="isOpenAICompatible" label="Model">
        <n-input v-model:value="ai_model" placeholder="gpt-4o-mini" />
      </n-form-item>
    </n-form>
  </n-card>
</template>
