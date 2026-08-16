import { useState } from 'react'
import { useLanguage } from '../i18n.jsx'
import { fetchExplainReport } from '../api.js'

export default function ReportDecoder() {
  const { lang, t } = useLanguage()
  const [rawText, setRawText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const SECTIONS = [
    { key: 'what_found', icon: '🔍', title: t('sec_what') },
    { key: 'actual_impact', icon: '💡', title: t('sec_impact') },
    { key: 'next_steps', icon: '🏥', title: t('sec_next') },
    { key: 'lifestyle', icon: '🥗', title: t('sec_lifestyle') },
  ]

  async function handleDecode() {
    if (!rawText.trim()) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const data = await fetchExplainReport(rawText, lang)
      setResult(data)
    } catch {
      setError(t('rd_error'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="panel">
      <h2 className="panel-title">{t('rd_title')}</h2>
      <p className="panel-desc">{t('rd_desc')}</p>
      <textarea
        className="report-input"
        rows={4}
        value={rawText}
        onChange={(e) => setRawText(e.target.value)}
        placeholder={t('rd_placeholder')}
      />
      <button className="btn-primary" onClick={handleDecode} disabled={loading || !rawText.trim()}>
        {loading ? t('rd_loading') : t('rd_btn')}
      </button>
      {error && <p className="error">{error}</p>}

      {result && (
        <div className="decode-result">
          {result.offline_fallback && <p className="hint">{t('rd_offline')}</p>}
          {SECTIONS.map((s) =>
            result[s.key] ? (
              <div className="decode-block" key={s.key}>
                <h4>
                  {s.icon} {s.title}
                </h4>
                <p>{result[s.key]}</p>
              </div>
            ) : null,
          )}
          <div className="disclaimer">{result.disclaimer}</div>
        </div>
      )}
    </section>
  )
}
