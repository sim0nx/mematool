<%inherit file="/base.mako" />
<%def name="actions()">
	<p id="actions">
		${h.link_to('Add single payment',url(controller='payments', action='editPayment', member_id=c.member.uid, mode='single'))}
	</p>
</%def>
<p id="lastsuntil">
	% if c.unverifiedPledges > 0:
		This member has ${c.unverifiedPledges} unverified pledges. 
	% endif
	At the current rate of ${c.ppm} EUR/month, her/his membership will end on ${c.member.leavingDate}.
</p>

<table class="table_content" width="95%">
	<thead>
		<tr>
			<th>Date</th><th>Amount</th><th>Type</th><th>Reason</th><th>by method</th><th>Tools</th>
		</tr>
	</thead>
	<tbody>
	%for p in c.payments:
		<tr>
			<td>${p.dtdate}</td>
			<td>${p.dtamount} EUR</td>
			<td>${p.dtmode}</td>
			<td style="font-style:italic;">${p.dtreason}</td>
			<td>${p.dtpaymentmethod.dtname}</td>
			% if (p.dtmode == 'recurring'):
				% if p.dtverified == 1:
					checked = True
				% else:
					checked = False
				% endif
				<td>${h.checkbox('verify[]', value='1', checked=checked, label='Verified', id=p.idpayment)}
			% else:
				<td>${h.link_to('Modify',url(controller='payments', action='editPayment', idpayment=p.idpayment, member_id=c.member.uid))}</td>
			% endif
		</tr>
	%endfor
	</tbody>
</table>
