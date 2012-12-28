<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if hasattr(c, var):
    return getattr(c, var)
%>

<h3>${c.heading}</h3>

${h.form(url(controller='mails', action='doEditAlias'), method='post', name='editAliasForm')}

<table class="table table-striped">
  ${parent.all_messages()}
  % if c.mode == 'add':
  <tr>
    <td><label for="alias">${_('Alias name:')}</label></td>
    <td>
      ${h.text('alias', value=getFormVar(session, c, 'alias'), class_='text')}@
    </td>
  </tr>
  <tr>
    <td><label for="alias">${_('Domain name:')}</label></td>
    <td>
      ${h.select('domain', selected_values=getFormVar(session, c, 'domain'), options=c.select_domains, class_='text')}
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
      ${h.textarea('mail', content=getFormVar(session, c, 'mail'), rows='10', cols='60', class_='text')}
    </td>
  </tr>
  <tr>
    <td>
      ${_('Mail destination')}
    </td>
    <td>
      ${h.textarea('maildrop', content=getFormVar(session, c, 'maildrop'), rows='10', cols='60', class_='text')}
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
    ${h.hidden('alias', value=getFormVar(session, c, 'alias'))}
    % endif
    % if getFormVar(session, c, 'mode') == 'edit':
    ${h.hidden('domain', value=getFormVar(session, c, 'domain'))}
    % endif
    ${h.hidden('mode', value=getFormVar(session, c, 'mode'))}
    <button type="submit" class="btn">${label}</button>
    </td>
  </tr>
</table>
${h.end_form()}
