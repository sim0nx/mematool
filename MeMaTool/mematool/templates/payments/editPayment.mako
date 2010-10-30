<%inherit file="/base.mako" />
<%def name="actions()" >
	<p id="actions">
		<a href="${url(controller='payments', action='listPayments', member_id=c.payment.limember)}">&lt;-- back to Payments</a>
	</p>
</%def>

${h.form(url(controller='payments', action='savePayment'), method='post', name='addpaymentform')}
<table class="table_content" width="95%">
        <tr>
                <td class="table_label"><label for="dtamount">Amount payed</label></td>
		<td>${h.text('dtamount', value=c.payment.dtamount, class_='input')}</td>
        </tr>
        <tr>
                <td class="table_label"><label for="dtdate">Date payed</label></td>
		<td>${h.text('dtdate', value=c.payment.dtdate, class_='input')}(dd/mm/yyyy, replace by datepicker)</td>
        </tr>
        <tr>
                <td class="table_label"><label for="dtreason">Reason for payment</label></td>
		<td><textarea name="dtreason" class="input" >${c.payment.dtreason}</textarea></td>
        </tr>
        <tr>
                <td class="table_label"><label for="lipaymentmethod">payment method</label></td>
		<td>${h.select("lipaymentmethod", 'paypal', c.methods)}</td>
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
	<input type="hidden" name="limember" value="${c.payment.limember}">
	<input type="hidden" name="idpayment" value="${c.payment.idpayment}">
	<input type="hidden" name="dtmode" value="single">
</table>
${h.end_form()}
