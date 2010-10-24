<% self.seen_css = set() %>

<!DOCTYPE html PUBLIC "XHTML 1.0 Transitional" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
        <head>
        	<title>syndicat MeMaTool</title>
            	${self.css()}
        </head>
        <body>
		${self.header()}
		${self.heading()}
		${self.menu()}
		${self.breadcrumbs()}
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
<%def name="breadcrumbs()"></%def>
<%def name="footer()"><p><a href="#top">Top ^</a></p></%def>
