<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if hasattr(c, var):
    return getattr(c, var)

  return ''
%>

<form action="/mails/doEditAlias" method="post" name="editAliasForm">

<table class="table table-striped">
  ${parent.all_messages()}
  % if c.mode == 'add':
  <tr>
    <td><label for="alias">${_('Alias name:')}</label></td>
    <td>
      <input type="text" name="alias" value="${getFormVar(session, c, 'alias')}" class="form-control">@
    </td>
  </tr>
  <tr>
    <td><label for="alias">${_('Domain name:')}</label></td>
    <td>
      <select name="domain" class="form-control">
        % for k, v in c.select_domains:
        <%
          if k == getFormVar(session, c, 'domain'):
            selected = 'selected'
          else:
            selected = ''
        %>
        <option value="${k}" ${selected}>${v}</option>
      % endfor
      </select>
    </td>
  </tr>
  % else:
  <tr>
    <td><label for="alias">${_('Alias name:')}</label></td>
    <td>
      ${c.alias}
    </td>
  </tr>
  % endif
  <tr>
    <td>
      ${_('Related aliases')}
    </td>
    <td>
      <textarea name="mail" rows="10" cols="60" class="form-control">${getFormVar(session, c, 'mail')}</textarea>
    </td>
  </tr>
  <tr>
    <td>
      ${_('Mail destination')}
    </td>
    <td>
      <textarea name="maildrop" rows="10" cols="60" class="form-control">${getFormVar(session, c, 'maildrop')}</textarea>
    </td>
  </tr>
  <tr>
    <td/>
    <td>
    <% 
      if not hasattr(c, 'alias') or c.alias == None:
        label = _('Add alias')
      else:
        label = _('Edit alias')
    %>
    % if hasattr(c, 'alias') and not c.alias == None:
    <input type="hidden" name="alias" value="${getFormVar(session, c, 'alias')}">
    % endif
    % if getFormVar(session, c, 'mode') == 'edit':
    <input type="hidden" name="domain" value="${getFormVar(session, c, 'domain')}">
    % endif
    <input type="hidden" name="mode" value="${getFormVar(session, c, 'mode')}">
    <button type="submit" class="btn btn-default">${label}</button>
    </td>
  </tr>
</table>
</form>
