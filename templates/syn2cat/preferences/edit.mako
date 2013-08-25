<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if hasattr(c, var):
    return vars(c)[var]

  return ''
%>

<form method="post" action="/preferences/doEdit" name="recordform">
<table class="table">
  ${parent.all_messages()}
  <tr>
    <td class="table_title">
      ${_('Language')}
    </td>
    <td>
      <select name="language" class="form-control">
      % for l in c.languages:
      <%
        if getFormVar(session, c, 'language') == l:
          selected = 'selected'
        else:
          selected = ''
      %>
      <option name="${l}" ${selected}>${l}</option>
      % endfor
      </select>
    </td>
  </tr>
  <tr>
    <td></td>
    <td><button type="submit" class="btn btn-default">${_('Submit')}</button></td>
  </tr>
</table>
</form>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
