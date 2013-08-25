<%inherit file="/base.mako" />

<table class="table table-striped"> 
  <tr>
    <th>${_('Key')}</th>
    <th>${_('Value')}</th>
  </tr>
  <tr>
    <td>${_('All members')}</td>
    <td>${c.members}</td>
  </tr>
  <tr>
    <td>${_('Active members')}</td>
    <td>${c.activeMembers}</td>
  </tr>
  <tr>
    <td>${_('Former members')}</td>
    <td>${c.formerMembers}</td>
  </tr>
  <tr>
    <td>${_('Payments OK')}</td>
    <td>${c.paymentsOk}</td>
  </tr>
  <tr>
    <td>${_('Payments NOT OK')}</td>
    <td>${c.paymentsNotOk}</td>
  </tr>
</table>
