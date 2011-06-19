<% self.seen_css = set() %>

<!DOCTYPE HTML>
<html lang="en-US">
<head>
	<meta charset="UTF-8">
	<meta name="" content="" />
	<meta name="" content="" />
	<meta name="" content="" />
	<meta name="" content="" />
	<meta name="" content="" />
	
	<!-- Stylesheets !-->
	<link rel="stylesheet" href="/css/screen.css" type="text/css" media="screen, projection">
  	<link rel="stylesheet" href="/css/app.css" type="text/css" media="screen, projection"> 
	<link rel="stylesheet" href="/css/ui.css" type="text/css" media="screen, projection">

	<!-- Website title !-->
	<title>syn2cat MeMaTool - {PAGENAME}</title>
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
			<nav id="top" class="span-16 push-2 last">
				<ul class="list-horizontal">
					% if session.has_key('identity'):
					<li><a href="#">Dashboard</a></li>
					<li>${h.link_to('Members',url(controller='members', action='showAllMembers'))}</li>
					<li>${h.link_to('Payments',url(controller='payments', action='showOutstanding'))}</li>
					<li>${h.link_to('Statistics',url(controller='statistics', action='getOverview',id=None))}</li>
					<li>${h.link_to('Profile',url(controller='profile', action='index'))}</li>
					% endif
					<li>${h.link_to('Logout',url(controller='auth', action='logout',id=None))}</li>
				</ul>
			</nav>
			
		</div>
		<!-- header end !-->
		
		<!-- main content !-->
		<section id="main" class="span-24 prepend-top">
			

			<!-- sidebar !-->
			% if hasattr(c, 'actions'):
			<aside id="sidebar" class="span-4">
				<nav class="menu">
					<header class="sidebar-title">Menu</header>
					<ul class="list-vertical">
						% for k in c.actions:
					        <li>${h.link_to(k[0], url(controller=k[1], action=k[2]))}</li>
						% endfor
					</ul>
				</nav>
				
			</aside>
			% endif
			<!-- sidebar end !-->
			
			<!-- content !-->
		${self.header()}
		${self.flash()}
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
	<script type="text/javascript" src="/javascript/jquery.js"></script>
        <script type="text/javascript" src="/javascript/ui.jquery.js"></script>
        <script type="text/javascript" src="/javascript/mematool.js"></script>
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
    <div id="flash"><p>${session.get('flash')}</p></div>
    <%
        del session['flash']
        session.save()
    %>
    % endif
</%def>

<% 
	# We should be able to dynmically get all available controllers and list them (where?) 
%>
