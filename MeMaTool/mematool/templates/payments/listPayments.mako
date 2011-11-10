<%inherit file="/base.mako" />

<div id="content" class="span-19 push-1 last ">
	<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
	<article>
		<li><table class="table_content">
			${parent.flash()}
			<tr>
				<th class="table_title">${_('Date')}</th>
				<th class="table_title">${_('by method')}</th>
				<th class="table_title">${_('validated')}</th>
				<th class="table_title">${_('Tools')}</th>
			</tr>
			% for i in range(1, 13):
			<%
			p_id = None

			if i in c.payments:
				p = c.payments[i]

				p_id = p.idpayment
				validated = h.literal('<img src="/images/icons/notok.png">') if not p.dtverified else h.literal('<img src="/images/icons/ok.png">')
				payment_method = p.dtpaymentmethod.dtname
			else:
				validated = 'no record'
				payment_method = 'no record'
			%>
			<tr class="table_row">
				<td>${str(c.year) + '-' + str(i)}</td>
				<td>${payment_method}</td>
				<td>${validated}</td>
				% if not p_id is None:
				<td>${h.link_to(_('Modify'),url(controller='payments', action='editPayment', idPayment=p_id, member_id=c.member_id))}</td>
				% if session.has_key('isFinanceAdmin') and session['isFinanceAdmin']:
				<td>${h.link_to(_('Duplicate'),url(controller='payments', action='duplicatePayment', idPayment=p_id, member_id=c.member_id))}</td>
				<td>${h.link_to(_('Validate'),url(controller='payments', action='validatePayment', idPayment=p_id, member_id=c.member_id))}</td>
				<td>${h.link_to(_('Delete'),url(controller='payments', action='deletePayment', idPayment=p_id, member_id=c.member_id))}</td>
				% endif
				% else:
				<td>${h.link_to(_('Add'),url(controller='payments', action='editPayment', year=c.year, month=i, member_id=c.member_id))}</td>
				% endif
			</tr>
			%endfor
		</table>
		<div class="clear">&nbsp;</div>
	</article>
</div>
