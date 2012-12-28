<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if hasattr(c, var):
    return getattr(c, var)

  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if var in vars(c.payment):
    return vars(c.payment)[var]

%>


<%def name="actions()" >
  <p id="actions">
    <a href="${url(controller='payments', action='listPayments', member_id=c.member_id)}">&lt;-- ${_('back to Payments')}</a>
  </p>
</%def>


<h3>${c.heading}</h3>
${h.form(url(controller='payments', action='savePayment'), method='post', name='addpaymentform')}

<table class="table table-striped"> 
  ${parent.all_messages()}
  <tr>
    <td><label for="date">${_('Month payed')}</label></td>
    <td>${h.text('date', value=getFormVar(session, c, 'date'))}(YYYY-MM-01)</td>
  </tr>
  <tr>
    <td><label for="Status">${_('Status')}</label></td>
    <td>
      ${h.radio('status', value=0, checked=c.status_0)}${_('Normal payment')}<br>
      ${h.radio('status', value=1, checked=c.status_1)}${_('No payment')}<br>
      ${h.radio('status', value=2, checked=c.status_2)}${_('Not a member')}<br>
    </td>
  </tr>
  % if session.has_key('isFinanceAdmin') and session['isFinanceAdmin']:
  <tr>
    <td><label for="verified">${_('Payment verified')}</label></td>
    <td>${h.checkbox('verified', value='1', checked=getFormVar(session, c, 'verified'))}</td>
  </tr>
  % endif
  <tr>
    <td>
    <td>
    <% 
      if (c.payment.id == None):
        label = _('Add payment')
      else:
        label = _('Edit payment')
    %>
    <button type="submit" class="btn">${label}</button>
  </tr>
  ${h.hidden('member_id', value=c.member_id)}
  ${h.hidden('idPayment', value=c.payment.id)}
</table>
${h.end_form()}
