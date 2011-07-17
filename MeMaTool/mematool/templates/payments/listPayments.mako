<%inherit file="/base.mako" />

<div id="content" class="span-19 push-1 last ">
	<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
	<article>
		<li><table class="table_content">
			${parent.flash()}
			<tr>
				<th class="table_title">Date</th>
				<th class="table_title">Amount</th>
				<th class="table_title">Reason</th>
				<th class="table_title">by method</th>
				<th class="table_title">validated</th>
				<th class="table_title">Tools</th>
			</tr>
			%for p in c.payments:
			<%
			validated = h.literal('<img src="/images/icons/notok.png">') if not p.dtverified else h.literal('<img src="/images/icons/ok.png">')
			%>
			<tr class="table_row">
				<td>${p.dtdate}</td>
				<td>${p.dtamount} EUR</td>
				<td style="font-style:italic;">${p.dtreason}</td>
				<td>${p.dtpaymentmethod.dtname}</td>
				<td>${validated}</td>
				<td>${h.link_to('Modify',url(controller='payments', action='editPayment', idPayment=p.idpayment, member_id=c.member_id))}</td>
				% if session.has_key('isAdmin') and session['isAdmin']:
				<td>${h.link_to('Duplicate',url(controller='payments', action='duplicatePayment', idPayment=p.idpayment, member_id=c.member_id))}</td>
				<td>${h.link_to('Validate',url(controller='payments', action='validatePayment', idPayment=p.idpayment, member_id=c.member_id))}</td>
				<td>${h.link_to('Delete',url(controller='payments', action='deletePayment', idPayment=p.idpayment, member_id=c.member_id))}</td>
				% endif
			</tr>
			%endfor
		</table>
		<div class="clear">&nbsp;</div>
	</article>
</div>
