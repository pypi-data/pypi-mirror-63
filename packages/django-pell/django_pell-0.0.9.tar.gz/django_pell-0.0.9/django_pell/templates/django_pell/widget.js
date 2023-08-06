document.addEventListener(`DOMContentLoaded`, () => {
  const editor = pell.init({
    element: document.getElementById(`pell-editor__{{ widget.name }}`),
    onChange: html => {
      document
        .querySelector(`[name="{{ widget.name }}"]`)
        .value = html;
    },
    defaultParagraphSeparator: `{{ widget.default_paragraph_separator }}`,
    styleWithCSS:{% if widget.style_with_css is True %} true{% else %} false{% endif %},
    classes: {
      actionbar: 'pell-actionbar',
      button: 'pell-button',
      content: 'pell-content',
      selected: 'pell-button-selected'
    },
    {% if widget.actions %}actions: [{% for action in widget.actions %}`{{ action}}`,{% endfor %}]{% endif %}
  });

  {% if widget.value %}
  editor.content.innerHTML =  `{{ widget.value|safe }}`
  {% endif %}
})


