<%inherit file="/base.mako" />

<%def name="actions()">
<p id="actions">
<form action="/payments/editPayment" method="post" name="addpayment">
  <select name="member_id">
  % for k, v in c.member_ids.items():
   <option value="${k}">${v}</option>
  % endfor
  </select>
  <input type="submit" name="choose" value="Add payment">
</form>
</p>
</%def>

<table class="table table-striped"> 
  <thead>
    <tr> 
      <th>#</th>
      <th>${_('Username')}</th>
      <th>${_('Surname')}</th>
      <th>${_('Given name')}</th>
      <th>${_('E-Mail')}</th>
      <th>${_('Payment good')}</th>
      <th>${_('Tools')}</th>
    </tr>
    <tbody>
    <% i = 0 %>
    % for m in c.members:
      <%
        paymentGood = r'<font color="red">' + _('no') + r'</font>' if not m.paymentGood else r'<font color="green">' + _('yes') + r'</font>'
        i += 1
      %>
    <tr class="table_row">
      <td>${i}</td>
      <td><a href="/members/editMember/?member_id=${m.uid}">${m.uid}</a></td>
      <td>${m.sn}</td>
      <td>${m.gn}</td>
      <td>${m.mail}</td>
      <td>${paymentGood}</td>
      <td><a href="/payments/listPayments/?member_id=${m.uid}">${_('payments')}</a></td>
    </tr>
    % endfor
  </tbody>
</table>
