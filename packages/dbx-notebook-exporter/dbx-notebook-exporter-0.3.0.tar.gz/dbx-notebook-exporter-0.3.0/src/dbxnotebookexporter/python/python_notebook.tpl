{%- extends 'null.tpl' -%}

{%- block in_prompt -%}
#%%
{%- endblock in_prompt -%}

{% block input %}
{{ cell.source | ipython2python }}
{% endblock input %}

{% block markdowncell scoped %}
{{ cell.source | comment_lines }}
{% endblock markdowncell %}
