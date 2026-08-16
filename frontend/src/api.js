const BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1'

async function getJSON(path) {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error(`请求失败: ${res.status}`)
  return res.json()
}

export async function fetchAssociations() {
  return getJSON('/associations')
}

export async function fetchSearch(query) {
  return getJSON(`/search?q=${encodeURIComponent(query)}`)
}

export async function fetchChecklistText(symbol) {
  const data = await getJSON(`/checklist/${encodeURIComponent(symbol)}/text`)
  return data.text
}

export async function fetchMyths() {
  return getJSON('/myths')
}

export async function fetchInheritance(payload) {
  const res = await fetch(`${BASE}/calculate/inheritance`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(`请求失败: ${res.status}`)
  return res.json()
}

export async function fetchExplainReport(rawText) {
  const res = await fetch(`${BASE}/report/explain`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ raw_text: rawText }),
  })
  if (!res.ok) throw new Error(`请求失败: ${res.status}`)
  return res.json()
}

export async function askChatStream(message, onChunk, onDone) {
  const res = await fetch(`${BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  })
  if (!res.ok || !res.body) throw new Error(`请求失败: ${res.status}`)

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop()
    for (const line of lines) {
      if (!line.startsWith('data:')) continue
      const payload = line.slice(5).trim()
      if (!payload || payload === '[DONE]') continue
      try {
        const data = JSON.parse(payload)
        if (data.content) onChunk(data.content)
        if (data.done) { onDone && onDone(); return }
      } catch {
        /* ignore malformed chunk */
      }
    }
  }
  onDone && onDone()
}
