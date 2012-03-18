<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
	if hasattr(c, var):
		return getattr(c, var)

	if 'reqparams' in s:
		if var in s['reqparams']:
			return s['reqparams'][var]
%>


<%def name="actions()" >
	<p id="actions">
		<a href="${url(controller='payments', action='listPayments', member_id=c.member_id)}">&lt;-- ${_('back to Payments')}</a>
	</p>
</%def>

${h.form(url(controller='payments', action='doBulkAdd'), method='post', name='addpaymentform')}
<div id="content" class="span-19 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
<article>

<table class="table_content" width="95%">
	${parent.all_messages()}
        <tr>
                <td class="table_title"><label for="months">${_('How many months')}</label></td>
		<td>${h.text('months', value=getFormVar(session, c, 'months'), class_='text')}</td>
        </tr>
	% if session.has_key('isFinanceAdmin') and session['isFinanceAdmin']:
	<tr>
		<td class="table_title"><label for="verified">${_('Payment(s) verified')}</label></td>
		<td>${h.checkbox('verified', value='1', checked=getFormVar(session, c, 'verified'), class_='text')}</td>
	</tr>
	% endif
	<tr>
		<td class="table_title"/>
		<td style="text-align:left;">
		${h.submit('send', _('Add payment'), class_='text')}</td>
	</tr>
	${h.hidden('member_id', value=c.member_id)}
</table>
${h.end_form()}
