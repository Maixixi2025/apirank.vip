const fs = require('fs');

const statePath = '/root/apirank/drafts/state.json';
const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));

const drafts = state.drafts;

// Collect all 20 articles we need to publish (filter by slug)
const slugsToPublish = [
  'deepseek-vs-openai-vs-google-ai',
  'anthropic-claude-api-review',
  'zhipu-glm-4-api-review',
  'tencent-hunyuan-api-review',
  'volcengine-doubao-api-review',
  'openai-gpt-4o-review',
  'openrouter-review',
  'baidu-wenxin-ernie-api-review',
  'freemodel-api-review',
  'apikeyfun-api-review',
  'ai-api-free-tiers-2026',
  'cerebras-api-review',
  'ai-api-speed-benchmarks-2026',
  'openai-moderation-api-2026',
  'sambanova-api-review',
  'openrouter-q2-2026-token-share-leaderboard',
  'claude-apple-foundation-models-2026',
  'gpt-5-api-pricing-2026',
  'openai-price-cut-analysis-2026',
  'claude-fable-5-mythos-5-2026'
];

const remainingDrafts = [];
const newlyPublished = [];

for (const draft of drafts) {
  if (slugsToPublish.includes(draft.slug)) {
    const entry = { ...draft };
    entry.status = 'published';
    entry.published_at = draft.date;
    
    // Fix anthropic-claude-api-review en_astro path
    if (entry.slug === 'anthropic-claude-api-review') {
      entry.en_astro = 'src/pages/tutorials/anthropic-claude-api-review.astro';
    }
    
    // Remove any fields that shouldn't be in published
    delete entry.note;
    
    newlyPublished.push(entry);
  } else {
    remainingDrafts.push(draft);
  }
}

// Add newly published to the beginning of published array
state.published = [...newlyPublished, ...state.published];
state.drafts = remainingDrafts;
state.updated = new Date().toISOString();

fs.writeFileSync(statePath, JSON.stringify(state, null, 2) + '\n');

console.log(`Moved ${newlyPublished.length} articles from drafts to published`);
console.log(`${remainingDrafts.length} remaining in drafts`);
