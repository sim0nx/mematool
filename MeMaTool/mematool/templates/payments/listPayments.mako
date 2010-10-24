<%inherit file="/base.mako" />
<%def name="menu()">
	${parent.menu()}
	<p>
		<a href="${url(controller='payments', action='editPayment', member_id=c.member_id)}">Add payment</a>
	</p>
</%def>
<table class="table_content" width="95%">
	<thead>
		<tr>
			<th>Date</th><th>Amount</th><th>Reason</th><th>by method</th><th>Tools</th>
		</tr>
	</thead>
	<tbody>
	%for p in c.payments:
		<tr>
			<td>${p.dtdate}</td>
			<td>${p.dtamount} EUR</td>
			<td style="font-style:italic;">${p.dtreason}</td>
			<td>need to to relational query first</td>
			<td><a href="${url(controller='payments', action='editPayment', idpayment=p.idpayment)}">Edit</a></td>
		</tr>
	%endfor
	</tbody>
</table>
