import { useLanguage } from '../i18n.jsx'

export default function MetaphorCard({ assoc, mode, onOpenChecklist }) {
  const { lang, t } = useLanguage()
  const { gene, disease, evidence, lifestyle_prevention } = assoc

  const isPro = mode === 'pro'
  const geneName = lang === 'zh'
    ? gene.chinese_name || gene.name || ''
    : gene.name || gene.chinese_name || ''
  const diseaseName = lang === 'zh'
    ? disease.chinese_name || disease.name
    : disease.name || disease.chinese_name

  const metaphorTitle = lang === 'en' ? gene.metaphor_title_en || gene.metaphor_title : gene.metaphor_title
  const metaphorStory = lang === 'en' ? gene.metaphor_story_en || gene.metaphor_story : gene.metaphor_story
  const plainSummary = lang === 'en' ? gene.plain_summary_en || gene.plain_summary : gene.plain_summary
  const screeningAdvice = lang === 'en'
    ? lifestyle_prevention?.screening_advice_en || lifestyle_prevention?.screening_advice
    : lifestyle_prevention?.screening_advice

  const severityBadge = lang === 'en'
    ? disease.severity_badge_en || disease.severity_badge
    : disease.severity_badge
  const plainRating = lang === 'en'
    ? evidence?.plain_rating_en || evidence?.plain_rating
    : evidence?.plain_rating

  const hasPlainContent = metaphorTitle || metaphorStory || plainSummary
  const hasChecklist = screeningAdvice

  let body
  if (isPro) {
    body = (
      <p className="card-body">
        {gene.academic_summary || `${gene.symbol}: ${evidence?.professional_rating || t('no_pro_summary')}`}
      </p>
    )
  } else if (hasPlainContent) {
    body = (
      <>
        <h4 className="metaphor-title">{metaphorTitle || t('no_metaphor')}</h4>
        <p className="card-body">{metaphorStory || plainSummary}</p>
      </>
    )
  } else {
    body = (
      <p className="card-body">{plainSummary || t('bulk_no_metaphor')}</p>
    )
  }

  return (
    <article className="card">
      <div className="card-head">
        <div>
          <h3>
            {gene.symbol} {geneName && geneName !== gene.symbol && <span className="gene-cn">{geneName}</span>}
          </h3>
          <div className="disease">{diseaseName}</div>
        </div>
        <span className="badge">{severityBadge || t('badge_pending')}</span>
      </div>

      {body}

      <div className="rating">
        {isPro ? (
          <span>
            {t('overall_score')} {evidence?.overall_score?.toFixed?.(2) ?? '—'} · ClinVar{' '}
            {evidence?.clinvar_pathogenic_count ?? '—'}
          </span>
        ) : (
          <span>{plainRating || t('no_rating')}</span>
        )}
      </div>

      {!isPro && hasChecklist && onOpenChecklist && (
        <>
          <div className="prevention">
            <strong>{t('screening_advice')}</strong>
            {screeningAdvice}
          </div>
          <button className="btn-outline" onClick={onOpenChecklist}>
            {t('open_checklist')}
          </button>
        </>
      )}
    </article>
  )
}
