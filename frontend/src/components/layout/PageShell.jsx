function PageShell({ eyebrow, title, children }) {
  return (
    <section className="page-shell">
      <header className="page-shell__header">
        {eyebrow ? <p className="page-shell__eyebrow">{eyebrow}</p> : null}
        <h1 className="page-shell__title">{title}</h1>
      </header>

      <div className="page-shell__body">{children}</div>
    </section>
  )
}

export default PageShell