<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
	if 'reqparams' in s:
		if var in s['reqparams']:
			return s['reqparams'][var]

	if var in vars(c.payment):
		return vars(c.payment)[var]

%>


<%def name="actions()" >
	<p id="actions">
		<a href="${url(controller='payments', action='listPayments', member_id=c.member_id)}">&lt;-- ${_('back to Payments')}</a>
	</p>
</%def>

${h.form(url(controller='payments', action='savePayment'), method='post', name='addpaymentform')}
<div id="content" class="span-19 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
<article>

<table class="table_content" width="95%">
	${parent.all_messages()}
        <tr>
                <td class="table_title"><label for="dtamount">${_('Amount payed')}</label></td>
		<td>${h.text('dtamount', value=getFormVar(session, c, 'dtamount'), class_='input text')}</td>
        </tr>
        <tr>
                <td class="table_title"><label for="dtdate">${_('Date payed')}</label></td>
		<td>${h.text('dtdate', value=getFormVar(session, c, 'dtdate'), class_='input text')}(YYYY-MM-DD)</td>
        </tr>
        <tr>
                <td class="table_title"><label for="dtreason">${_('Reason for payment')}</label></td>
		<td><textarea name="dtreason" class="input text" >${getFormVar(session, c, 'dtreason')}</textarea></td>
        </tr>
        <tr>
                <td class="table_title"><label for="lipaymentmethod">${_('payment method')}</label></td>
		<td>${h.select("lipaymentmethod", getFormVar(session, c, 'lipaymentmethod'), c.methods, class_='input text')}</td>
        </tr>
	<tr>
		<td class="table_title"/>
		<td style="text-align:left;">
		<% 
			if (c.payment.idpayment == None):
				label = _('Add payment')
			else:
				label = _('Edit payment')
		%>
		${h.submit('send', label, class_='input text')}</td>
	</tr>
	<input type="hidden" name="member_id" value="${c.member_id}">
	<input type="hidden" name="idPayment" value="${c.payment.idpayment}">
</table>
${h.end_form()}
