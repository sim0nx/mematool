<!DOCTYPE HTML>
<html lang="en-US">
<head>
  <meta charset="UTF-8">
  <!-- Stylesheets !-->
  <link href="/css/bootstrap.min.css" rel="stylesheet" media="screen">
  <link href="/css/mematool_bootstrap_custom.css" rel="stylesheet" media="screen" type="text/css"/>
  <script type="text/javascript" src="/javascript/jquery.min.js"></script>
  <script type="text/javascript" src="/javascript/mematool.js"></script>
  <script type="text/javascript" src="/javascript/bootstrap.min.js"></script>
  <!-- Website title !-->
  <title>syn2cat MeMaTool</title>
</head>
<body>

<div id="wrap">
  <div class="container bs-docs-container">
    <div class="row">
      <div class="col-md-12">
        <!-- Title -->
        <div class="page-header">
          <h1><img src="/images/logo.png" width="" height="" alt="mematool logo" /></h1>

          <!-- NavBar -->
          <header class="navbar navbar-inverse bs-docs-nav" role="banner">
            <div class="container">
              <div class="navbar-header">
                <button class="navbar-toggle" type="button" data-toggle="collapse" data-target=".bs-navbar-collapse">
                  <span class="sr-only">Toggle navigation</span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                </button>
              </div>
              <nav class="collapse navbar-collapse bs-navbar-collapse" role="navigation">
                <ul class="nav navbar-nav">
                  % if session.has_key('username'):
                    % if session.get('user').is_in_group('isFinanceAdmin') or session.get('user').is_admin():
                    <li class=""><a href="/members/showAllMembers">${_('Members')}</a></li>
                    <li class=""><a href="/statistics/index">${_('Statistics')}</a></li>
                    % endif
                    % if session.get('user').is_admin():
                    <li class=""><a href="/mails/index">${_('Mails')}</a></li>
                    % endif
                    <li class=""><a href="/payments/index">${_('Payments')}</a></li>
                    <li class=""><a href="/profile/index">${_('Profile')}</a></li>
                    <li class=""><a href="/doLogout">${_('Logout')}</a></li>
                  % else:
                    <li class=""><a href="/">${_('Login')}</a></li>
                  % endif
                </ul>
                <ul class="nav navbar-nav navbar-right">
                  <li><a href="/setLang?lang=en"><img src="/images/icons/flags/en.png" alt="en"/></a></li>
                  <li><a href="/setLang?lang=lu"><img src="/images/icons/flags/lu.png" alt="lu"/></a></li>
                  <li><a href="/setLang?lang=de"><img src="/images/icons/flags/de.png" alt="de"/></a></li>
                </ul>
              </nav>
            </div>
          </header>
          <!-- NavBar -->
        </div>
        <!-- Title -->
      </div>
    </div>

    % if c.is_admin:
    <%include file="/pendingMemberValidations.mako" />
    % endif

    <div class="row">
      <div class="col-md-2">
        <div class="bs-sidebar hidden-print" role="complementary">
          <!-- sidebar !-->
          % if len(sidebar) > 0:
          <ul class="nav bs-sidenav">
            <li class="nav-header">Menu</li>
            % for l in sidebar:
            <%
              params = ''
              for k, v in l.get('args').get('params', {}).items():
                if params == '':
                  params ='/?'
                else:
                  params += '&'

                params += '{0}={1}'.format(k, v)
            %>
            <li><a href="/${l.get('args').get('controller')}/${l.get('args').get('action')}${params}" onclick="${l.get('onclick', None)}">${l['name']}</a></li>
            % endfor
          </ul>
          % endif
        </div>
      </div>
      <!-- content !-->
      <div class="col-md-10" role="main">
      ${self.header()}
      % if hasattr(c, 'heading'):
      <h3>${c.heading}</h3>
      % endif
      ${flash()}
      ${next.body()}
      ${self.footer()}
      <!-- content end !-->
      </div>
    </div>
  </div>
  <div id="push"></div>
</div>

  <!-- footer !-->
<div id="footer">
  <div class="container col-md-offset-2">
    <div class="row" style="margin: 0 auto;">
      <div class="col-md-10">
        MeMaTool (c) 2010-2013 Georges Toth
      </div>
    </div>
  </div>
</div>
  <!-- footer !-->
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
<%
  if session.has_key('flash'):
    if session.has_key('flash_class'):
      if session.get('flash_class') == 'error':
        flash_class = 'danger'
      else:
        flash_class = session.get('flash_class')
    else:
      flash_class = 'info'
%>
% if session.has_key('flash'):
<div class="alert alert-${flash_class}">${session.get('flash')}</div>
% endif
<%
  if session.has_key('flash'):
    del session['flash']
    session.save()
%>
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
