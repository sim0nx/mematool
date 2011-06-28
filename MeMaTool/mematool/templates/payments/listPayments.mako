<%inherit file="/base.mako" />

<div id="content" class="span-19 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
<article>
<table class="table_content" width="95%">
	<tr>
		<td class="table_title">Date</td>
		<td class="table_title">Amount</td>
		<td class="table_title">Type</td>
		<td class="table_title">Reason</td>
		<td class="table_title">by method</td>
		<td class="table_title">Tools</td>
	</tr>
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
			<td>${h.link_to('Modify',url(controller='payments', action='editPayment', idPayment=p.idpayment, member_id=c.member.uid))}</td>
			<td>${h.link_to('Delete',url(controller='payments', action='deletePayment', idPayment=p.idpayment, member_id=c.member.uid))}</td>
		% endif
	</tr>
	%endfor
</table>
</article>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>
