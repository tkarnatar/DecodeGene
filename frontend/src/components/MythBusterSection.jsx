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
        {myths.map((m, i) => {
          const myth = lang === 'en' ? m.myth_en || m.myth : m.myth
          const truth = lang === 'en' ? m.truth_en || m.truth : m.truth
          return (
            <div className="myth-card" key={i}>
              <p className="myth">❌ {myth}</p>
              <p className="truth">✅ {truth}</p>
              {m.chinese_name && (
                <span className="myth-gene">
                  {t('myth_related')}
                  {lang === 'zh' ? m.chinese_name : m.gene}
                </span>
              )}
            </div>
          )
        })}
      </div>
    </section>
  )
}
