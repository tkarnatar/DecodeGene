import { useEffect, useState } from 'react'
import MetaphorCard from './components/MetaphorCard.jsx'
import ReportDecoder from './components/ReportDecoder.jsx'
import DoctorChecklistModal from './components/DoctorChecklistModal.jsx'
import FamilySimulator from './components/FamilySimulator.jsx'
import MythBusterSection from './components/MythBusterSection.jsx'
import AskDoctor from './components/AskDoctor.jsx'
import { useLanguage } from './i18n.jsx'
import { fetchAssociations, fetchSearch } from './api.js'

export default function App() {
  const { lang, setLang, t } = useLanguage()
  const [mode, setMode] = useState('simple')
  const [associations, setAssociations] = useState([])
  const [query, setQuery] = useState('')
  const [results, setResults] = useState(null)
  const [checklistGene, setChecklistGene] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAssociations()
      .then(setAssociations)
      .catch(() => setAssociations([]))
      .finally(() => setLoading(false))
  }, [])

  async function handleSearch(e) {
    e.preventDefault()
    const q = query.trim()
    if (!q) return
    try {
      const data = await fetchSearch(q)
      setResults(data)
    } catch {
      setResults({ query: q, count: 0, results: [] })
    }
  }

  const shown = results ? results.results : associations

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="brand-logo">🧬</span>
          <span className="brand-name">{t('brand_name')}</span>
        </div>
        <div className="topbar-actions">
          <button
            className="lang-btn"
            onClick={() => setLang(lang === 'zh' ? 'en' : 'zh')}
            aria-label="switch language"
          >
            {lang === 'zh' ? 'English' : '中文'}
          </button>
          <div
            className="mode-switch"
            role="button"
            tabIndex={0}
            onClick={() => setMode(mode === 'simple' ? 'pro' : 'simple')}
            onKeyDown={(e) => e.key === 'Enter' && setMode(mode === 'simple' ? 'pro' : 'simple')}
          >
            <span className={mode === 'simple' ? 'mode-active' : ''}>{t('mode_simple')}</span>
            <span className="mode-track">
              <span className={`mode-thumb ${mode === 'pro' ? 'thumb-pro' : ''}`} />
            </span>
            <span className={mode === 'pro' ? 'mode-active' : ''}>{t('mode_pro')}</span>
          </div>
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <h1>{t('hero_title')}</h1>
          <p>{t('hero_sub')}</p>
          <form className="search-bar" onSubmit={handleSearch}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={t('search_placeholder')}
            />
            <button type="submit">{t('search_btn')}</button>
            {results && (
              <button
                type="button"
                className="ghost"
                onClick={() => {
                  setResults(null)
                  setQuery('')
                }}
              >
                {t('clear_btn')}
              </button>
            )}
          </form>
        </section>

        {loading && <p className="hint">{t('loading')}</p>}

        {results && (
          <p className="hint">{t('search_result', { query: results.query, count: results.count })}</p>
        )}

        <section className="cards-grid">
          {shown.map((assoc) => (
            <MetaphorCard
              key={assoc.association_id}
              assoc={assoc}
              mode={mode}
              onOpenChecklist={() => setChecklistGene(assoc.gene.symbol)}
            />
          ))}
          {!loading && shown.length === 0 && <p className="hint">{t('empty')}</p>}
        </section>

        <ReportDecoder />
        <FamilySimulator />
        <MythBusterSection />
        <AskDoctor />

        <footer className="footer">{t('footer_disclaimer')}</footer>
      </main>

      {checklistGene && (
        <DoctorChecklistModal
          geneSymbol={checklistGene}
          onClose={() => setChecklistGene(null)}
        />
      )}
    </div>
  )
}
