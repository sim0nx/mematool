<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if var in vars(c.group):
    return vars(c.group)[var]
%>


<form action="/groups/doEditGroup" method="post" name="editGroupForm">

<table class="table table-striped"> 
  ${parent.all_messages()}
  <tr>
    <td class="table_title"><label for="gid">${_('Group name:')}</label></td>
    <td><input type="text" name="gid" value="${getFormVar(session, c, 'gid')}" class="form-control"></td>
  </tr>
  % if hasattr(c.group, 'gidNumber') and not c.group.gidNumber == None:
  <tr>
    <td class="table_title">
      ${_('Group members')}
    </td>
    <td>
      <textarea name="users" rows="10" cols="60" class="form-control">${getFormVar(session, c, 'users')}</textarea>
    </td>
  </tr>
  % endif
  <tr>
    <td class="table_title"/>
    <td style="text-align:left;">
    <% 
      if not hasattr(c.group, 'gidNumber') or c.group.gidNumber == None:
        label = _('Add group')
      else:
        label = _('Edit group')
    %>
    <button type="submit" class="btn btn-default">${_('Edit group')}</button>
  </tr>
</table>
</form>
