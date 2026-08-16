import { useEffect, useState } from 'react'
import { useLanguage } from '../i18n.jsx'
import { fetchMyths } from '../api.js'

export default function MythBusterSection() {
  const { lang, t } = useLanguage()
  const [myths, setMyths] = useState([])

  useEffect(() => {
    fetchMyths().then(setMyths).catch(() => setMyths([]))
  }, [])

  if (myths.length === 0) return null

  return (
    <section className="panel">
      <h2 className="panel-title">{t('myth_title')}</h2>
      <p className="panel-desc">{t('myth_desc')}</p>
      <div className="myths-grid">
        {myths.map((m, i) => (
          <div className="myth-card" key={i}>
            <p className="myth">❌ {m.myth}</p>
            <p className="truth">✅ {m.truth}</p>
            {m.chinese_name && (
              <span className="myth-gene">
                {t('myth_related')}
                {lang === 'zh' ? m.chinese_name : m.gene}
              </span>
            )}
          </div>
        ))}
      </div>
    </section>
  )
}
