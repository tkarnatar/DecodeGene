import { useState } from 'react'
import { useLanguage } from '../i18n.jsx'
import { fetchInheritance } from '../api.js'

export default function FamilySimulator() {
  const { t } = useLanguage()
  const [pattern, setPattern] = useState('AD')
  const [father, setFather] = useState('normal')
  const [mother, setMother] = useState('normal')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const patterns = ['AD', 'AR', 'XR', 'XD']
  const statuses = ['normal', 'carrier', 'affected']

  async function handleCalculate() {
    setLoading(true)
    try {
      const data = await fetchInheritance({
        pattern,
        father_status: father,
        mother_status: mother,
      })
      setResult(data)
    } catch {
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="panel">
      <h2 className="panel-title">{t('fs_title')}</h2>
      <p className="panel-desc">{t('fs_desc')}</p>

      <div className="sim-controls">
        <label>
          {t('pattern_label')}
          <select value={pattern} onChange={(e) => setPattern(e.target.value)}>
            {patterns.map((p) => (
              <option key={p} value={p}>
                {t(`pattern_${p}`)}
              </option>
            ))}
          </select>
        </label>
        <label>
          {t('father_label')}
          <select value={father} onChange={(e) => setFather(e.target.value)}>
            {statuses.map((s) => (
              <option key={s} value={s}>
                {t(`status_${s}`)}
              </option>
            ))}
          </select>
        </label>
        <label>
          {t('mother_label')}
          <select value={mother} onChange={(e) => setMother(e.target.value)}>
            {statuses.map((s) => (
              <option key={s} value={s}>
                {t(`status_${s}`)}
              </option>
            ))}
          </select>
        </label>
        <button className="btn-primary" onClick={handleCalculate} disabled={loading}>
          {loading ? t('calc_loading') : t('calc_btn')}
        </button>
      </div>

      {result && (
        <div className="sim-result">
          <div className="bars">
            <div className="bar-row">
              <span className="bar-label">{t('bar_affected')}</span>
              <div className="bar">
                <div className="bar-fill risk" style={{ width: `${result.child_disease_risk_pct}%` }} />
              </div>
              <span className="bar-value">{result.child_disease_risk_pct}%</span>
            </div>
            <div className="bar-row">
              <span className="bar-label">{t('bar_carrier')}</span>
              <div className="bar">
                <div className="bar-fill carrier" style={{ width: `${result.child_carrier_risk_pct}%` }} />
              </div>
              <span className="bar-value">{result.child_carrier_risk_pct}%</span>
            </div>
            <div className="bar-row">
              <span className="bar-label">{t('bar_normal')}</span>
              <div className="bar">
                <div className="bar-fill normal" style={{ width: `${result.child_normal_pct}%` }} />
              </div>
              <span className="bar-value">{result.child_normal_pct}%</span>
            </div>
          </div>
          <p className="sim-explanation">{result.plain_explanation}</p>
          {result.by_sex && (
            <p className="hint">
              {t('boy_girl_hint', {
                male: result.by_sex.male?.disease_risk_pct,
                female: result.by_sex.female?.disease_risk_pct,
                carrier: result.by_sex.female?.carrier_risk_pct,
              })}
            </p>
          )}
          <ul className="recommendations">
            {result.recommendations?.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}
    </section>
  )
}
