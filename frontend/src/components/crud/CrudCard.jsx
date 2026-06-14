function CrudCard({ title, children, className = '' }) {
  return (
    <div className={`crud-card ${className}`.trim()}>
      <h2>{title}</h2>
      {children}
    </div>
  )
}

export default CrudCard