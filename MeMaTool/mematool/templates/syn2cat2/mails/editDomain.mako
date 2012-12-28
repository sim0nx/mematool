<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if hasattr(c, 'domain') and var in vars(c.domain):
    return vars(c.domain)[var]
%>

<% 
  if not hasattr(c, 'domain') or c.domain == None:
    label = _('Add domain')
  else:
    label = _('Edit domain')
%>


<h3>${c.heading}</h3>

${h.form(url(controller='mails', action='doEditDomain'), method='post', name='editDomainForm')}
<table class="table">
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
  <tr>
    <td></td>
    <td><button type="submit" class="btn">${label}</button></td>
  </tr>
</table>

% if hasattr(c, 'domain') and hasattr(c.domain, 'dc') and not c.domain.dc == None:
${h.hidden('dc', value=getFormVar(session, c, 'dc'))}
% endif
${h.end_form()}
