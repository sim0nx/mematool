<%inherit file="/base.mako" />

<%def name="actions()">
<p id="actions">
${h.form(url(controller='payments', action='editPayment'), method='post', name='addpayment')}
  ${h.select('member_id', '1000', c.member_ids)}
  ${h.submit('choose','Add payment')}
${h.end_form()}
</p>
</%def>

<div id="content" class="span-19 push-1 last ">
  <header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
  <article>
    <li><table class="table_content"> 
            <tr> 
        <th class="table_title">
          #
        </th>
                    <th class="table_title">
                            ${_('Username')}
                    </th>
                    <th class="table_title">
                            ${_('Surname')}
                    </th>
                    <th class="table_title">
                            ${_('Given name')}
                    </th>
        <th class="table_title">
          ${_('E-Mail')}
        </th>
                    <th class="table_title">
                            ${_('Payment good')}
                    </th>
                    <th colspan="3" class="table_title">
                            ${_('Tools')}
                    </th>
            </tr>
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
    </table>
    <div class="clear">&nbsp;</div>
  </article>
</div>
