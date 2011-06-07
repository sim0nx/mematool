<% self.seen_css = set() %>

<!DOCTYPE html PUBLIC "XHTML 1.0 Transitional" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
        <head>
        	<title>syndicat MeMaTool</title>
            	${self.css()}
        </head>
        <body>
		${self.header()}
		% if session.has_key('identity'):
		${self.menu()}
		% endif
		${self.heading()}
		${self.actions()}
		${self.breadcrumbs()}
		${self.flash()}
		${next.body()}
		${self.footer()}
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
<%def name="menu()"></%def>
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
% if session.has_key('identity'):
<%def name="menu()">
	<p id="menu">
	  ${h.link_to('Members',url(controller='members', action='showAllMembers'))}
	| ${h.link_to('Payments',url(controller='payments', action='showOutstanding'))}
	| ${h.link_to('Payment-methods',url(controller='paymentmethods', action='listMethods',id=None))}
	| ${h.link_to('Statistics',url(controller='statistics', action='getOverview',id=None))}
	| ${h.link_to('Profile',url(controller='profile', action='index'))}
	| ${h.link_to('Logout',url(controller='auth', action='logout',id=None))}
	</p>
</%def>
%endif
