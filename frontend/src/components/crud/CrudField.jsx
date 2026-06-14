function CrudField({
  label,
  name,
  value,
  onChange,
  type = 'text',
  as = 'input',
  placeholder,
  options = [],
  rows = 4,
  min,
  className = '',
}) {
  return (
    <label className={`crud-field ${className}`.trim()}>
      <span>{label}</span>

      {as === 'textarea' ? (
        <textarea
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          rows={rows}
        />
      ) : as === 'select' ? (
        <select name={name} value={value} onChange={onChange}>
          {placeholder ? <option value="">{placeholder}</option> : null}
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      ) : (
        <input
          type={type}
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          min={min}
        />
      )}
    </label>
  )
}

export default CrudField