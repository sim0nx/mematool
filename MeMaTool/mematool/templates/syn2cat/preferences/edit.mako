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

<form method="post" action="${url(controller='preferences', action='doEdit')}" name="recordform">
<div id="content" class="span-18 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
<article>
<table class="table_content" width="95%">
  ${parent.all_messages()}
  <tr>
    <td class="table_title">
      ${_('Language')}
    </td>
    <td>
      ${h.select('language', selected_values=getFormVar(session, c, 'language'), options=c.languages, class_='text')}
    </td>
  </tr>
</table>
<input type="submit" name="" value="${_('Submit')}" class="input button right">
</article>
</form>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
