<%inherit file="/base.mako" />
<%def name="actions()">
	<p id="actions">
		<a href="${url(controller='payments', action='editPayment', member_id=c.member_id)}">Add payment</a>
	</p>
</%def>
<p id="lastsuntil">
This member chose to pay ${c.member.dtmonthly} EUR per month. (<a href="${url(controller='members', action='setMonthlyFee', member_id=c.member_id)}">edit</a>)<br/>
At the current rate, this will last <strong>until ${c.until}</strong>. (Add nice graphics or calendar)
</p>

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
			<td>need to do relational query first</td>
			<td><a href="${url(controller='payments', action='editPayment', idpayment=p.idpayment)}">Edit</a></td>
		</tr>
	%endfor
	</tbody>
</table>
