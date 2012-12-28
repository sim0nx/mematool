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

<h3>${c.heading}</h3>

<form method="post" action="${url(controller='preferences', action='doEdit')}" name="recordform">
<table class="table">
  ${parent.all_messages()}
  <tr>
    <td class="table_title">
      ${_('Language')}
    </td>
    <td>
      ${h.select('language', selected_values=getFormVar(session, c, 'language'), options=c.languages, class_='text')}
    </td>
  </tr>
  <tr>
    <td></td>
    <td><button type="submit" class="btn">${_('Submit')}</button></td>
  </tr>
</table>
</form>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
