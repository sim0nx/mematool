<%inherit file="/base.mako" />

<div id="content" class="span-19 push-1 last ">
	<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
	<article>
		<li><table class="table_content">
			${parent.flash()}
			<tr>
				<th class="table_title">Date</th>
				<th class="table_title">Amount</th>
				<th class="table_title">Type</th>
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
				<td>${p.dtmode}</td>
				<td style="font-style:italic;">${p.dtreason}</td>
				<td>${p.dtpaymentmethod.dtname}</td>
				<td>${validated}</td>
				% if (p.dtmode == 'recurring'):
					% if p.dtverified == 1:
						checked = True
					% else:
						checked = False
					% endif
				<td>${h.checkbox('verify[]', value='1', checked=checked, label='Verified', id=p.idpayment)}
				% else:
				<td>${h.link_to('Modify',url(controller='payments', action='editPayment', idPayment=p.idpayment, member_id=c.member.uid))}</td>
					% if session.has_key('isAdmin') and session['isAdmin']:
				<td>${h.link_to('Duplicate',url(controller='payments', action='duplicatePayment', idPayment=p.idpayment, member_id=c.member.uid))}</td>
				<td>${h.link_to('Validate',url(controller='payments', action='validatePayment', idPayment=p.idpayment, member_id=c.member.uid))}</td>
				<td>${h.link_to('Delete',url(controller='payments', action='deletePayment', idPayment=p.idpayment, member_id=c.member.uid))}</td>
					% endif
				% endif
			</tr>
			%endfor
		</table>
		<div class="clear">&nbsp;</div>
	</article>
</div>
