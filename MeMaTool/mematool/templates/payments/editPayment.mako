<%inherit file="/base.mako" />
<%def name="menu()" >
	${parent.menu()}
	<p>
		<a href="${url(controller='payments', action='listPayments', member_id=c.payment.limember)}">&lt;-- back to Payments</a>
	</p>
</%def>

<%
	## Supposedly, there is also a form helper:
	"""
	${h.form(h.url(action='email'), method='get')}
		Email Address: ${h.text_field('email')}
               ${h.submit('Submit')}
	${h.end_form()}
	"""

%>
<form method="post" action="${url(controller='payments', action='savePayment')}" name="recordform">
<table class="table_content" width="95%">
        <tr>
                <td class="table_label"><label for="dtamount">Amount payed</label></td>
		<td><input type="text" name="dtamount" class="input" value="${c.payment.dtamount}" /></td>
        </tr>
        <tr>
                <td class="table_label"><label for="dtdate">Date payed</label></td>
		<td><input type="text" name="dtdate" class="input" value="${c.payment.dtdate}"/>(replace by datepicker)</td>
        </tr>
        <tr>
                <td class="table_label"><label for="dtreason">Reason for payment</label></td>
		<td><textarea name="dtreason" class="input" >${c.payment.dtreason}</textarea></td>
        </tr>
        <tr>
                <td class="table_label"><label for="lipaymentmethod">payment method</label></td>
		<td><select name="lipaymentmethod">
			<option value="1">PayPal</option> <!-- added temporarily -->
		% for m in c.methods:
			<option value="${m.idpaymentmethod}">${m.dtname}</option>
		% endfor	
		 </select></td>
        </tr>
	<tr>
		<td class="table_label"/>
		<td style="text-align:left;"><button name="send" label="Add payment">
		% if (c.payment.idpayment == ''):
			Add
		% else:
			Edit
		% endif
		payment</button></td>
	</tr>
	<input type="hidden" name="limember" value="${c.payment.limember}">
	<input type="hidden" name="idpayment" value="${c.payment.idpayment}">
</table>
</form>
