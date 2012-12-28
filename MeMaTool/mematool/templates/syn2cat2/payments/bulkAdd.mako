<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if hasattr(c, var):
    return getattr(c, var)

  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]
%>


<%def name="actions()" >
  <p id="actions">
    <a href="${url(controller='payments', action='listPayments', member_id=c.member_id)}">&lt;-- ${_('back to Payments')}</a>
  </p>
</%def>

<h3>${c.heading}</h3>
${h.form(url(controller='payments', action='doBulkAdd'), method='post', name='addpaymentform')}

<table class="table table-striped"> 
  ${parent.all_messages()}
  <tr>
    <td><label for="months">${_('How many months')}</label></td>
    <td>${h.text('months', value=getFormVar(session, c, 'months'))}</td>
  </tr>
  % if session.has_key('isFinanceAdmin') and session['isFinanceAdmin']:
  <tr>
    <td><label for="verified">${_('Payment(s) verified')}</label></td>
    <td>${h.checkbox('verified', value='1', checked=getFormVar(session, c, 'verified'))}</td>
  </tr>
  % endif
  <tr>
    <td></td>
    <td><button type="submit" class="btn">${_('Add payment')}</button></td>
  </tr>
  ${h.hidden('member_id', value=c.member_id)}
</table>
${h.end_form()}
