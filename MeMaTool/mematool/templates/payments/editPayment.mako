<%inherit file="/base.mako" />
<%def name="menu()" >
	${parent.menu()}
	<p>
		<a href="${url(controller='payments', action='listPayments', member_id=c.payment.limember)}">&lt;-- back to Payments</a>
	</p>
</%def>

<form method="post" action="${url(controller='payments', action='savePayment')}" name="recordform">
<table class="table_content" width="95%">
        <tr>
                <td class="table_label"><label for="dtamount">Amount payed</label></td>
		<td><input type="text" name="dtamount" class="input" /></td>
        </tr>
        <tr>
                <td class="table_label"><label for="dtdate">Amount payed</label></td>
		<td><input type="text" name="dtdate" class="input" /></td>
        </tr>
        <tr>
                <td class="table_label"><label for="dtreason">Amount payed</label></td>
		<td><textarea name="dtreason" class="input" ></textarea></td>
        </tr>
        <tr>
                <td class="table_label"><label for="lipaymentmethod">Amount payed</label></td>
		<td><input type="text" name="lipaymentmethod" class="input" /></td>
        </tr>
	<tr>
		<td class="table_label"/>
		<td style="text-align:left;"><button name="send" label="Add payment">Add payment</button></td>
	</tr>
	<input type="hidden" name="member_id" value="${c.payment.limember}">
</table>
</form>
