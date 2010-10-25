<% self.seen_css = set() %>

<!DOCTYPE html PUBLIC "XHTML 1.0 Transitional" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
        <head>
        	<title>syndicat MeMaTool</title>
            	${self.css()}
        </head>
        <body>
		${self.header()}
		${self.menu()}
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
<%def name="menu()">
	<p>
	  <a href="${h.url_for(controller='members', action='showAllMembers', id=None)}">Members</a>
	| <a href="${h.url_for(controller='payments', action='showOutstanding',id=None)}">Payments</a>
	| <a href="${h.url_for(controller='paymentmethods', action='listMethods',id=None)}">Payment-methods</a>
	</p>
</%def>

