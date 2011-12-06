<% self.seen_css = set() %>

<!DOCTYPE HTML>
<html lang="en-US">
<head>
	<meta charset="UTF-8">
	
	<!-- Stylesheets !-->
	<link rel="stylesheet" href="/css/screen.css" type="text/css" media="screen, projection">
  	<link rel="stylesheet" href="/css/app.css" type="text/css" media="screen, projection"> 
	<link rel="stylesheet" href="/css/ui.css" type="text/css" media="screen, projection">
	<link rel="stylesheet" href="/css/ie.css" type="text/css" media="screen, projection">
	
	<!-- Website title !-->
	<title>syn2cat MeMaTool</title>
</head>
<body>
	<!-- topbar !-->
	<div id="top"></div>
	<!-- topbar end !-->
	
	<!-- page-wrapper !-->
	<div id="wrapper" class="container prepend-top">
		
		<!-- header !-->
		<div id="header" class="span-24">
			
			<!-- logo !-->
			<div id="logo" class="span-8">
				<img src="/images/logo.png" width="" height="" alt="mematool logo" />
			</div>
			<!-- logo end !-->
			
			<!-- top-navigation !-->
			% if session.has_key('identity'):
			<nav id="top" class="span-16 push-2 last">
				<ul class="list-horizontal">
					<li><a href="#">${_('Dashboard')}</a></li>
						% if session['isFinanceAdmin'] or session['isAdmin']:
					<li>${h.link_to(_('Members'),url(controller='members', action='showAllMembers'))}</li>
						% endif
					<li>${h.link_to(_('Payments'),url(controller='payments', action='index'))}</li>
						% if session['isFinanceAdmin'] or session['isAdmin']:
					<li>${h.link_to(_('Statistics'),url(controller='statistics', action='getOverview',id=None))}</li>
						% endif
					<li>${h.link_to(_('Profile'),url(controller='profile', action='index'))}</li>
					<li>${h.link_to(_('Logout'),url(controller='auth', action='logout',id=None))}</li>
				</ul>
			</nav>
			% endif
			
		</div>
		<!-- header end !-->
		
		<!-- main content !-->
		<section id="main" class="span-24 prepend-top">
			

			<!-- sidebar !-->
			% if hasattr(c, 'actions'):
			<aside id="sidebar" class="span-4">
				<nav class="menu">
					<header class="sidebar-title">${_('Menu')}</header>
					<ul class="list-vertical">
						% if len(c.actions) > 0:
							% for k in c.actions:
								% if len(k) == 4:
					        <li>${h.link_to(k[0], url(controller=k[1], action=k[2], member_id=k[3]))}</li>
								% else:
					        <li>${h.link_to(k[0], url(controller=k[1], action=k[2]))}</li>
								% endif
							% endfor
						% else:
							<li>-</li>
						% endif
					</ul>
				</nav>
				
			</aside>
			% endif
			<!-- sidebar end !-->
			
			<!-- content !-->
			${self.header()}
			${next.body()}
			${self.footer()}
			<!-- content end !-->
			
		</section>
		<!-- main content end !-->
		
		<footer class="span-24">
			<a href="https://www.hackerspace.lu/"><img src="/images/footerlogo.png" width="" height="" alt="syn2cat logo"/></a>
		</footer>
	</div>
	<!-- page-wrapper end !-->
	<!-- JavaScript !-->
	<!--[if lt IE 9]>
	<script type="text/javascript" src="/mematool/javascript/html5.js"></script>
	<![endif]-->
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
	# We should be able to dynmically get all available controllers and list them (where?) 
%>
