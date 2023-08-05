{{#general_title}}
# {{{title}}}

{{/general_title}}

{{#versions}}
{{#solicited_requests}}### {{{solicited_requests}}}{{/solicited_requests}}

{{#sections}}
{{#commits}}

{{#tags}}## {{{tags}}} {{/tags}}
                  {{#tags}}Fecha de creacion: {{{date}}}{{/tags}}

  * {{date}} {{#links_or_not}}[{{{second_parameter}}}]({{{jira_url}}}/{{{second_parameter}}}){{/links_or_not}}{{^links_or_not}}{{{second_parameter}}}{{/links_or_not}} {{{commit_title}}}
{{/commits}}
{{/sections}}
{{/versions}}