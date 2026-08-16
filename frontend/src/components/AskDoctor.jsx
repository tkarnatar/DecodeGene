import { useEffect, useRef, useState } from 'react'
import { useLanguage } from '../i18n.jsx'
import { askChatStream } from '../api.js'

export default function AskDoctor() {
  const { t } = useLanguage()
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const scrollRef = useRef(null)

  useEffect(() => {
    setMessages([{ role: 'assistant', content: t('ai_welcome') }])
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [t('ai_welcome')])

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight
  }, [messages])

  async function handleSend(e) {
    e.preventDefault()
    const q = input.trim()
    if (!q || loading) return
    setInput('')
    setLoading(true)
    setMessages((m) => [...m, { role: 'user', content: q }, { role: 'assistant', content: '' }])

    let acc = ''
    try {
      await askChatStream(
        q,
        (chunk) => {
          acc += chunk
          setMessages((m) => {
            const copy = [...m]
            copy[copy.length - 1] = { role: 'assistant', content: acc }
            return copy
          })
        },
        () => setLoading(false),
      )
    } catch {
      setMessages((m) => {
        const copy = [...m]
        copy[copy.length - 1] = { role: 'assistant', content: t('ai_error') }
        return copy
      })
      setLoading(false)
    }
  }

  return (
    <section className="panel">
      <h2 className="panel-title">{t('ai_title')}</h2>
      <p className="panel-desc">{t('ai_desc')}</p>
      <div className="chat-box" ref={scrollRef}>
        {messages.map((m, i) => (
          <div key={i} className={`chat-row ${m.role === 'user' ? 'chat-user' : 'chat-ai'}`}>
            <div className="chat-bubble">
              {m.content || (loading && i === messages.length - 1 ? '…' : '')}
            </div>
          </div>
        ))}
      </div>
      <form className="chat-input" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t('ai_placeholder')}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? t('sending_btn') : t('send_btn')}
        </button>
      </form>
    </section>
  )
}
