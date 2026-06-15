function PaginationControls({
  currentPage,
  totalPages,
  onPageChange,
  itemLabel = 'elementos',
  totalItems,
}) {
  if (!totalPages || totalPages <= 1) {
    return null
  }

  return (
    <div className="pagination" role="navigation" aria-label={`Paginación de ${itemLabel}`}>
      <p className="pagination__summary">
        Página {currentPage} de {totalPages}
        {typeof totalItems === 'number' ? ` · ${totalItems} ${itemLabel}` : ''}
      </p>

      <div className="pagination__actions">
        <button
          type="button"
          onClick={() => onPageChange(Math.max(1, currentPage - 1))}
          disabled={currentPage <= 1}
        >
          Anterior
        </button>
        <button
          type="button"
          onClick={() => onPageChange(Math.min(totalPages, currentPage + 1))}
          disabled={currentPage >= totalPages}
        >
          Siguiente
        </button>
      </div>
    </div>
  )
}

export default PaginationControls
