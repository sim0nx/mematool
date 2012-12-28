<% self.seen_css = set() %>
<!DOCTYPE HTML>
<html lang="en-US">
<head>
  <meta charset="UTF-8">
  <!-- Stylesheets !-->
  <link href="/css/bootstrap.min.css" rel="stylesheet" media="screen" type="text/css"/>
  <!-- Website title !-->
  <title>syn2cat MeMaTool</title>
</head>
<body>

  <div class="container-fluid offset3">
    <div class="row-fluid" style="margin: 0 auto;">
      <div class="span10">
        <!-- Title -->
        <div class="page-header">
          <h1><img src="/images/logo.png" width="" height="" alt="mematool logo" /></h1>

          <!-- NavBar -->
          <div class="navbar navbar-inverse">
            <div class="navbar-inner">
              <div class="container">
                <a class="btn btn-navbar" data-toggle="collapse" data-target=".navbar-inverse-collapse">
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                </a>
                <div class="nav-collapse collapse navbar-inverse-collapse">
                  <div class="nav-collapse collapse">
                    % if session.has_key('identity'):
                    <ul class="nav">
                      <li><a href="#">${_('Dashboard')}</a></li>
                        % if session['isFinanceAdmin'] or session['isAdmin']:
                      <li>${h.link_to(_('Members'),url(controller='members', action='showAllMembers'))}</li>
                        % endif
                      <li>${h.link_to(_('Payments'),url(controller='payments', action='index'))}</li>
                        % if session['isFinanceAdmin'] or session['isAdmin']:
                      <li>${h.link_to(_('Statistics'),url(controller='statistics', action='index'))}</li>
                      <li>${h.link_to(_('Mails'),url(controller='mails', action='index'))}</li>
                        % endif
                      <li>${h.link_to(_('Profile'),url(controller='profile', action='index'))}</li>
                      <li>${h.link_to(_('Logout'),url(controller='auth', action='logout',id=None))}</li>
                      % else:
                      <li><a href="${url(controller='auth', action='login')}">Login</a></li>
                    </ul>
                    % endif
                    <ul class="nav">
                      <li><a href="/profile/setLang?lang=en"><img src="/images/icons/flags/en.png" alt="en"/></a></li>
                      <li><a href="/profile/setLang?lang=lb"><img src="/images/icons/flags/lu.png" alt="lb"/></a></li>
                      <li><a href="/profile/setLang?lang=de"><img src="/images/icons/flags/de.png" alt="de"/></a></li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- NavBar -->
        </div>
        <!-- Title -->
      </div>
    </div>
    <div class="row-fluid">
      <div class="span8 offset2">
        ${flash()}
      </div>
    </div>
    <div class="row-fluid">
      <div class="span1">
        <!-- sidebar !-->
        % if hasattr(c, 'actions') and len(c.actions) > 0:
        <ul class="nav nav-list">
          <li class="nav-header">Menu</li>
          % for l in c.actions:
          <li>${h.link_to(l['name'], url(**l['args']), onclick=l.get('onclick', None))}</li>
          % endfor
        </ul>
        % endif
      </div>
      <!-- content !-->
      <div class="span8 offset1">
      ${self.header()}
      ${next.body()}
      ${self.footer()}
      <!-- content end !-->
      </div>
    </div>
  </div>
</body>
</html>

  <script type="text/javascript" src="/javascript/jquery.js"></script>
  <script type="text/javascript" src="/javascript/ui.jquery.js"></script>
  <script type="text/javascript" src="/javascript/mematool.js"></script>
  <script type="text/javascript" src="/javascript/jquery.qtip.js"></script>
</body>
</html>



<%def name="css_link(path, media='')">
% if path not in self.seen_css:
<link rel="stylesheet" type="text/css" href="${path|h}" media="${media}"></link>
% endif
<% self.seen_css.add(path) %>
</%def>

<%def name="css()">
${css_link('/css/main.css', 'screen')}
</%def>

<%def name="heading()"><h1>${hasattr(c, 'heading') and c.heading or 'No Title'}</h1></%def>
<%def name="header()"><a name="top"></a></%def>
<%def name="actions()"></%def>
<%def name="breadcrumbs()"></%def>
<%def name="footer()"><p><a href="#top">Top ^</a></p></%def>

<%def name="flash()">
% if session.has_key('flash'):
  % if session.has_key('flash_class'):
    <% flash_class = session.get('flash_class') %>
  % else:
    <% flash_class = 'info' %>
  % endif
<div id="flash" class="${flash_class}"><p>${session.get('flash')}</p></div>
    <%
      del session['flash']
      session.save()
    %>
% endif
</%def>

<%def name="error_messages()">
% if 'errors' in session:
  % if len(session['errors']) > 0:
<tr>
  <td colspan="2">
    <div class="error">
    % for k in session['errors']:
      <p>${k}</p>
    % endfor
    </div>
  </td>
</tr>
  % endif
  <%
  del session['errors']
  session.save()
  %>
% endif
</%def>

<%def name="all_messages()">
${self.flash()}
${self.error_messages()}
</%def>

<%
if session.has_key('reqparams'):
  del session['reqparams']
  session.save()
%>
