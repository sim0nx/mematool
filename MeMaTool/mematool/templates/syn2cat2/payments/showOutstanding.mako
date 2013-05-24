<%inherit file="/base.mako" />

<%def name="actions()">
<p id="actions">
${h.form(url(controller='payments', action='editPayment'), method='post', name='addpayment')}
  ${h.select('member_id', '1000', c.member_ids)}
  ${h.submit('choose','Add payment')}
${h.end_form()}
</p>
</%def>

<h3>${c.heading}</h3>
<%include file="/pendingMemberValidations.mako" />
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
        paymentGood = h.literal('<font color="red">' + _('no') + '</font>') if not m.paymentGood else h.literal('<font color="green">' + _('yes') + '</font>')
        i += 1
      %>
    <tr class="table_row">
      <td>${i}</td>
      <td><a href="${url(controller='members', action='editMember', member_id=m.uid)}">${m.uid}</a></td>
      <td>${m.sn}</td>
      <td>${m.gn}</td>
      <td>${m.mail}</td>
      <td>${paymentGood}</td>
      <td><a href="${url(controller='payments', action='listPayments', member_id=m.uid)}">${_('payments')}</a></td>
    </tr>
    % endfor
  </tbody>
</table>
