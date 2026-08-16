import { useLanguage } from '../i18n.jsx'

export default function MetaphorCard({ assoc, mode, onOpenChecklist }) {
  const { lang, t } = useLanguage()
  const { gene, disease, evidence, lifestyle_prevention } = assoc

  const isPro = mode === 'pro'
  const geneName = lang === 'zh' ? gene.chinese_name : gene.name || ''
  const diseaseName = lang === 'zh' ? disease.chinese_name : disease.name || disease.chinese_name

  const body = isPro ? (
    <p className="card-body">{gene.academic_summary || t('no_pro_summary')}</p>
  ) : (
    <>
      <h4 className="metaphor-title">{gene.metaphor_title || t('no_metaphor')}</h4>
      <p className="card-body">{gene.metaphor_story || gene.plain_summary}</p>
    </>
  )

  return (
    <article className="card">
      <div className="card-head">
        <div>
          <h3>
            {gene.symbol} {geneName && <span className="gene-cn">{geneName}</span>}
          </h3>
          <div className="disease">{diseaseName}</div>
        </div>
        <span className="badge">{disease.severity_badge || t('badge_pending')}</span>
      </div>

      {body}

      <div className="rating">
        {isPro ? (
          <span>
            {t('overall_score')} {evidence?.overall_score?.toFixed?.(2) ?? '—'} · OpenTargets{' '}
            {evidence?.opentargets_score?.toFixed?.(2) ?? '—'}
          </span>
        ) : (
          <span>{evidence?.plain_rating || t('no_rating')}</span>
        )}
      </div>

      {!isPro && (
        <>
          <div className="prevention">
            <strong>{t('screening_advice')}</strong>
            {lifestyle_prevention?.screening_advice || '—'}
          </div>
          <button className="btn-outline" onClick={onOpenChecklist}>
            {t('open_checklist')}
          </button>
        </>
      )}
    </article>
  )
}
