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
    <a href="/payments/listPayments/?member_id=${c.member_id}">&lt;-- ${_('back to Payments')}</a>
  </p>
</%def>

<form action="/payments/doBulkAdd" method="post" name="addpaymentform">

<table class="table table-striped"> 
  ${parent.all_messages()}
  <tr>
    <td><label for="months">${_('How many months')}</label></td>
    <td><input type="text" name="months" value="${getFormVar(session, c, 'months')}"></td>
  </tr>
  % if session.get('user').is_finance_admin():
  <tr>
    <td><label for="verified">${_('Payment(s) verified')}</label></td>
    <td><input type="checkbox" name="verified" value="1" ${'checked' if getFormVar(session, c, 'verified') else ''}></td>
  </tr>
  % endif
  <tr>
    <td></td>
    <td><button type="submit" class="btn btn-default">${_('Add payment')}</button></td>
  </tr>
  <input type="hidden" name="member_id" value="${c.member_id}">
</table>
</form>
