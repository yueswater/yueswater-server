function Div(el)
  local ad_type = nil
  for _, class in ipairs(el.classes) do
    if class == "note" or class == "question" or class == "warning" then
      ad_type = class
      break
    end
  end

  if ad_type then
    local title = el.attributes["title"] or string.upper(ad_type)
    el.classes = {}
    el.attributes = {}
    return {
      pandoc.RawBlock('latex', '\\begin{' .. ad_type .. '}{' .. title .. '}'),
      el,
      pandoc.RawBlock('latex', '\\end{' .. ad_type .. '}')
    }
  end
end