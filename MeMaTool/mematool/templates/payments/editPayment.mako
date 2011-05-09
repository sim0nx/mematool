<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
	if var in vars(c.payment):
		return vars(c.payment)[var]

	if 'reqparams' in s:
		if var in s['reqparams']:
			return s['reqparams'][var]

%>


<%def name="actions()" >
	<p id="actions">
		<a href="${url(controller='payments', action='listPayments', member_id=c.member_id)}">&lt;-- back to Payments</a>
	</p>
</%def>

${h.form(url(controller='payments', action='savePayment'), method='post', name='addpaymentform')}
<table class="table_content" width="95%">
	% if 'errors' in session:
	% if len(session['errors']) > 0:
	<tr>
		<td>&nbsp;</td>
		<td>
		% for k in session['errors']:
		<font color="red">${k}</font><br>
		% endfor
		</td>
	</tr>
		<%
		del session['errors']
		session.save()
		%>
	% else:
		<%
                del session['errors']
                session.save()
                %>
	% endif
	% endif
        <tr>
                <td class="table_label"><label for="dtamount">Amount payed</label></td>
		<td>${h.text('dtamount', value=getFormVar(session, c, 'dtamount'), class_='input')}</td>
        </tr>
        <tr>
                <td class="table_label"><label for="dtdate">Date payed</label></td>
		<td>${h.text('dtdate', value=getFormVar(session, c, 'dtdate'), class_='input')}(YYYY-MM-DD, replace by datepicker)</td>
        </tr>
        <tr>
                <td class="table_label"><label for="dtreason">Reason for payment</label></td>
		<td><textarea name="dtreason" class="input" >${getFormVar(session, c, 'dtreason')}</textarea></td>
        </tr>
        <tr>
                <td class="table_label"><label for="lipaymentmethod">payment method</label></td>
		<td>${h.select("lipaymentmethod", getFormVar(session, c, 'lipaymentmethod'), c.methods)}</td>
        </tr>
	<tr>
		<td class="table_label"/>
		<td style="text-align:left;">
		<% 
			if (c.payment.idpayment == None):
				label = 'Add payment'
			else:
				label = 'Edit payment'
		%>
		${h.submit('send',label)}</td>
	</tr>
	<input type="hidden" name="member_id" value="${c.member_id}">
	<input type="hidden" name="idpayment" value="${c.payment.idpayment}">
	<input type="hidden" name="dtmode" value="single">
</table>
${h.end_form()}
