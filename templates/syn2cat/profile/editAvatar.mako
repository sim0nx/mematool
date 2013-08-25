<%inherit file="/base.mako" />

<form action="/profile/doEditAvatar" name="recordform" method="post" enctype="multipart/form-data">
    <table class="table">
      % if c.member.validate:
      <tr>
        <td colspan="2">
          <div class="notice">
            ${_('Your account is currently locked for validation')}
          </div>
        </td>
      </tr>
      % endif
      ${parent.all_messages()}
      <tr>
        <td>
          <img src="${c.member.avatarUrl}" alt="${_('user profile image')}">
        </td>
        <td>
          <a href="/profile/doDeleteAvatar">${_('delete avatar')}</a>
        </td>
      </tr>
      <tr>
        <td>
          ${_('Avatar:')}
        </td>
        <td>
          <input type="file" id="avatar" name="avatar">
        </td>
      </tr>
      <tr>
        <td></td>
        <td><button type="submit" class="btn btn-default">${_('Submit')}</button></td>
    </table>
</form>
