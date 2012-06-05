<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if hasattr(c, 'domain') and var in vars(c.domain):
    return vars(c.domain)[var]
%>


${h.form(url(controller='mails', action='doEditDomain'), method='post', name='editDomainForm')}
<div id="content" class="span-19 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
<article>
<table class="table_content">
${parent.all_messages()}
  <tr>
    <td class="table_title"><label for="domain">${_('Domain name:')}</label></td>
    <td>
    % if c.mode is 'add':
    ${h.text('domain', value=getFormVar(session, c, 'dc'), class_='text')}
    % else:
    ${getFormVar(session, c, 'dc')}
    % endif
    </td>
  </tr>
</table>
<% 
  if not hasattr(c, 'domain') or c.domain == None:
    label = _('Add domain')
  else:
    label = _('Edit domain')
%>
% if hasattr(c, 'domain') and hasattr(c.domain, 'dc') and not c.domain.dc == None:
${h.hidden('dc', value=getFormVar(session, c, 'dc'))}
% endif
${h.submit('send', label, class_='text')}

${h.end_form()}
</article>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>
