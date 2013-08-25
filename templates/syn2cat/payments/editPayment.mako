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
    <a href="/payments/listPayments/?member_id=${c.member_id}">&lt;-- ${_('back to Payments')}</a>
  </p>
</%def>


<form action="/payments/savePayment" method="post" name="addpaymentform">

<table class="table table-striped"> 
  ${parent.all_messages()}
  <tr>
    <td><label for="date">${_('Month payed')}</label></td>
    <td><input id="date" type="text" name="date" value="${getFormVar(session, c, 'date')}" class="form-control">(YYYY-MM-01)</td>
  </tr>
  <tr>
    <td><label for="Status">${_('Status')}</label></td>
    <td>
      <input type="radio" name="status" value="0" ${'checked' if c.status_0 else ''}>${_('Normal payment')}<br>
      <input type="radio" name="status" value="1" ${'checked' if c.status_1 else ''}>${_('No payment')}<br>
      <input type="radio" name="status" value="2" ${'checked' if c.status_2 else ''}>${_('Not a member')}<br>
    </td>
  </tr>
  % if session.has_key('isFinanceAdmin') and session['isFinanceAdmin']:
  <tr>
    <td><label for="verified">${_('Payment verified')}</label></td>
    <td><input type="checkbox" name="verified" value="1" ${'checked' if getFormVar(session, c, 'verified') else ''}></td>
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
    <button type="submit" class="btn btn-default">${label}</button>
  </tr>
  <input type="hidden" name="member_id" value="${c.member_id}">
  <input type="hidden" name="idPayment" value="${c.payment.id}">
</table>
</form>

<script type="text/javascript" src="/javascript/bootstrap-datepicker.js"></script>
<script>$('#date').datepicker({format: "yyyy-mm-01", autoclose: true});</script>
