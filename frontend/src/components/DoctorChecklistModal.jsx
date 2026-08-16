import { useEffect, useState } from 'react'
import { useLanguage } from '../i18n.jsx'
import { fetchChecklistText } from '../api.js'

export default function DoctorChecklistModal({ geneSymbol, onClose }) {
  const { lang, t } = useLanguage()
  const [text, setText] = useState('')
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    fetchChecklistText(geneSymbol, lang).then(setText).catch(() => setText(t('cl_failed')))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [geneSymbol, lang])

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      setCopied(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-head">
          <h3>{t('cl_title')}</h3>
          <button className="close" onClick={onClose}>✕</button>
        </div>
        <pre className="checklist-text">{text || t('cl_loading')}</pre>
        <div className="modal-actions">
          <button className="btn-primary" onClick={handleCopy}>
            {copied ? t('copied_btn') : t('copy_btn')}
          </button>
          <button className="btn-outline" onClick={() => window.print()}>
            {t('print_btn')}
          </button>
        </div>
      </div>
    </div>
  )
}
