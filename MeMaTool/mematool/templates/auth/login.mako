<%inherit file="/base.mako" />

<%def name="css()">
	${parent.css()}
	${self.css_link('/css/viewAll.css', 'screen')}
</%def>

  <div>
     <b>Log In</b>
  </div>
  <br/>
  <form method="POST" action="${url(controller='auth', action='doLogin')}">
    <table border="0">
    <tr>
      <td>User Name</td>
      <td><input type="text" name="login"></input></td>
    </tr>
    <tr>
      <td>Password</td>
      <td><input type="password" name="password"></input></td>
    </tr>
    <tr>
      <td></td>
      <td><input type="submit" name="submit" value="Log In"/></td>
    </tr>
    </table>
  </form>
  <pre>
  </pre>
