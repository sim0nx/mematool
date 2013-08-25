<%inherit file="/base.mako" />

<form action="/payments/listPayments" method="post">
<table class="table">
  <tr>
    <td><label for="year">${_('Year')}</label></td>
    <td><input type="text" name="year" value="${c.year}" class="form-control"></td>
  </tr>
</table>
<input type="hidden" name="member_id" value="${c.member_id}">
</form>

<a href="/payments/bulkAdd/?member_id=${c.member_id}">${_('Bulk add multiple months')}</a>

<table class="table table-striped"> 
  ${parent.flash()}
  <thead>
    <tr>
      <th>${_('Month')}</th>
      <th>${_('Validated')}</th>
      <th>${_('Status')}</th>
      <th>${_('Tools')}</th>
    </tr>
  </thead>
  <tbody>
  % for i in range(1, 13):
  <%
  p_id = None
  validated = 'no record'
  status = r'<img src="/images/icons/notok.png">'

  if i in c.payments:
    p = c.payments[i]

    p_id = p.id
    validated = r'<img src="/images/icons/notok.png">' if not p.verified else r'<img src="/images/icons/ok.png">'

    if p.status == 0:
      status = r'<img src="/images/icons/ok.png">'
    elif p.status == 2:
      status = '-'
  %>
  <tr>
    <td>${str(c.year) + '-' + str(i)}</td>
    <td>${validated}</td>
    <td>${status}</td>
    % if not p_id is None:
      % if p.verified != 1 or session.get('user').is_finance_admin():
      <td><a href="/payments/editPayment/?member_id=${c.member_id}&idPayment=${p_id}">${_('Modify')}</a></td>
      % endif
      % if session.get('user').is_finance_admin():
      <td><a href="/payments/validatePayment/?member_id=${c.member_id}&idPayment=${p_id}">${_('Validate')}</a></td>
      <td><a href="/payments/deletePayment/?member_id=${c.member_id}&idPayment=${p_id}">${_('Delete')}</a></td>
      % endif
    % else:
    <td><a href="/payments/editPayment/?member_id=${c.member_id}&year=${c.year}&month=${i}">${_('Add')}</a></td>
    % endif
  </tr>
  %endfor
  </tbody>
</table>
