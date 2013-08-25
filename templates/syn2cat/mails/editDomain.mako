<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if hasattr(c, 'domain') and var in vars(c.domain):
    return vars(c.domain)[var]

  return ''
%>

<% 
  if not hasattr(c, 'domain') or c.domain == None:
    label = _('Add domain')
  else:
    label = _('Edit domain')
%>


<form action="/mails/doEditDomain" method="post" name="editDomainForm">
<table class="table">
  ${parent.all_messages()}
  <tr>
    <td class="table_title"><label for="domain">${_('Domain name:')}</label></td>
    <td>
    % if c.mode is 'add':
    <input type="text" name="domain" value="${getFormVar(session, c, 'dc')}" class="form-control">
    % else:
    ${getFormVar(session, c, 'dc')}
    % endif
    </td>
  </tr>
  <tr>
    <td></td>
    <td><button type="submit" class="btn btn-default">${label}</button></td>
  </tr>
</table>

% if hasattr(c, 'domain') and hasattr(c.domain, 'dc') and not c.domain.dc == None:
<input type="hidden" name="dc" value="${getFormVar(session, c, 'dc')}">
% endif
</form>
